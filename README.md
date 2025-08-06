# DNSDumpster

Python client to query DNSDumpster.com for DNS records of a domain.

## Installation

'''bash
pip install .
'''

## Usage

### From the command line:

'''bash
dnsdumpster example.com
'''

### From Python:

'''python
from dnsdumpster import DNSDumpsterClient

client = DNSDumpsterClient()
results = client.query_domain("example.com")

if results:
    # Print all A records
    print("A Records:")
    for a in results.get('a_records', []):
        print(f"  {a['hostname']} -> {a['ip']}")

    # Print all MX records
    print("\nMX Records:")
    for mx in results.get('mx_records', []):
        print(f"  {mx['mx_record']} -> {mx['ip']}")

    # Print all NS records
    print("\nNS Records:")
    for ns in results.get('ns_records', []):
        print(f"  {ns['ns_record']} -> {ns['ip']}")

    # Print all TXT records
    print("\nTXT Records:")
    for txt in results.get('txt_records', []):
        print(f"  {txt}")

else:
    print("No results found or query failed.")
'''

---

### Quick extraction of subdomains and IPs:

'''python
ips, subdomains = client.get_simple_list("example.com")
print("Subdomains:")
for sub in subdomains:
    print(f"  {sub}")
print("IPs:")
for ip in ips:
    print(f"  {ip}")
'''

---

## Notes

- The query_domain() method returns a dictionary with detailed DNS records.
- Use the keys 'a_records', 'mx_records', 'ns_records', 'txt_records', and 'ips_and_subdomains' to access specific data.
- The get_simple_list() method returns two lists: all IPs and all subdomains found.
