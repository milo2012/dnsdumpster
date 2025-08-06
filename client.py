import requests
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple


class DNSDumpsterClient:
    """Client for interacting with DNSDumpster API"""

    def __init__(self):
        self.base_url = "https://dnsdumpster.com"
        self.api_url = "https://api.dnsdumpster.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            'Te': 'trailers',
            'Connection': 'keep-alive'
        })
        self.auth_token = None

    def get_authorization_token(self) -> Optional[str]:
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            auth_pattern = r'"Authorization":\s*"([^"]+)"'
            match = re.search(auth_pattern, response.text)
            if match:
                self.auth_token = match.group(1)
                return self.auth_token
            else:
                return None
        except Exception:
            return None

    def query_domain(self, domain: str) -> Optional[Dict]:
        if not self.auth_token:
            if not self.get_authorization_token():
                return None

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Hx-Request': 'true',
            'Hx-Target': 'results',
            'Hx-Current-Url': 'https://dnsdumpster.com/',
            'Authorization': self.auth_token,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://dnsdumpster.com',
            'Referer': 'https://dnsdumpster.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Priority': 'u=0',
            'Te': 'trailers',
            'Connection': 'keep-alive'
        }

        data = {'target': domain}

        try:
            response = self.session.post(
                f"{self.api_url}/htmld/",
                headers=headers,
                data=data
            )
            response.raise_for_status()
            return self.parse_dns_results(response.text)
        except Exception:
            return None

    def parse_dns_results(self, html_content: str) -> Dict:
        soup = BeautifulSoup(html_content, 'html.parser')
        results = {
            'a_records': [],
            'mx_records': [],
            'ns_records': [],
            'txt_records': [],
            'ips_and_subdomains': []
        }

        a_table = soup.find('table', {'id': 'a_rec_table'})
        if a_table:
            tbody = a_table.find('tbody')
            if tbody:
                for row in tbody.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        hostname = cells[0].get_text(strip=True)
                        ip_cell = cells[1].get_text(strip=True)
                        ip = ip_cell.split('\n')[0] if '\n' in ip_cell else ip_cell

                        asn = cells[2].get_text(strip=True) if len(cells) > 2 else ''
                        asn_name = cells[3].get_text(strip=True) if len(cells) > 3 else ''

                        record = {
                            'hostname': hostname,
                            'ip': ip,
                            'asn': asn,
                            'asn_name': asn_name
                        }
                        results['a_records'].append(record)
                        results['ips_and_subdomains'].append({
                            'type': 'A',
                            'hostname': hostname,
                            'ip': ip
                        })

        mx_tables = soup.find_all('table')
        for table in mx_tables:
            prev_element = table.find_previous('p')
            if prev_element and 'MX Records' in prev_element.get_text():
                tbody = table.find('tbody')
                if tbody:
                    for row in tbody.find_all('tr'):
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            mx_record = cells[0].get_text(strip=True)
                            ip_cell = cells[1].get_text(strip=True)
                            ip = ip_cell.split('\n')[0] if '\n' in ip_cell else ip_cell

                            record = {
                                'mx_record': mx_record,
                                'ip': ip
                            }
                            results['mx_records'].append(record)
                            results['ips_and_subdomains'].append({
                                'type': 'MX',
                                'hostname': mx_record,
                                'ip': ip
                            })

        for table in mx_tables:
            prev_element = table.find_previous('p')
            if prev_element and 'NS Records' in prev_element.get_text():
                tbody = table.find('tbody')
                if tbody:
                    for row in tbody.find_all('tr'):
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            ns_record = cells[0].get_text(strip=True)
                            ip_cell = cells[1].get_text(strip=True)
                            ip = ip_cell.split('\n')[0] if '\n' in ip_cell else ip_cell

                            record = {
                                'ns_record': ns_record,
                                'ip': ip
                            }
                            results['ns_records'].append(record)
                            results['ips_and_subdomains'].append({
                                'type': 'NS',
                                'hostname': ns_record,
                                'ip': ip
                            })

        for table in mx_tables:
            prev_element = table.find_previous('p')
            if prev_element and 'TXT Records' in prev_element.get_text():
                tbody = table.find('tbody')
                if tbody:
                    for row in tbody.find_all('tr'):
                        cells = row.find_all('td')
                        if len(cells) >= 1:
                            txt_content = cells[0].get_text(strip=True)
                            txt_content = txt_content.replace('&#34;', '"')
                            results['txt_records'].append(txt_content)

        return results

    def get_simple_list(self, domain: str) -> Tuple[List[str], List[str]]:
        results = self.query_domain(domain)
        if not results:
            return [], []

        ips = []
        subdomains = []

        for record in results['ips_and_subdomains']:
            ip = record.get('ip')
            hostname = record.get('hostname')
            if ip and ip not in ips:
                ips.append(ip)
            if hostname and hostname not in subdomains:
                subdomains.append(hostname)

        return ips, subdomains
