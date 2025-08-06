# DNSDumpster

Python client and command-line tool to query [DNSDumpster.com](https://dnsdumpster.com) for DNS records of a domain.

## Installation

```bash
pip install .
```

---

## Usage

### 🔧 From the command line:

```bash
dnsdumpster example.com
```

Example:

```bash
$ dnsdumpster yahoo.com

A Records:
  img.3721.yahoo.com -> 202.43.217.119
  vl-107.bas2-1-edg.a4e.yahoo.com -> 98.137.87.132
  ...

MX Records:
  mta7.am0.yahoodns.net -> 98.136.96.76
  ...

NS Records:
  ns1.yahoo.com -> 68.180.131.16
  ...

TXT Records:
  "v=spf1 redirect=_spf.mail.yahoo.com"
  ...
```

---

### 🐍 From Python:

```python
from dnsdumpster import DNSDumpsterClient

client = DNSDumpsterClient()
results = client.query_domain("example.com")

if results:
    print("A Records:")
    for a in results.get('a_records', []):
        print(f"  {a['hostname']} -> {a['ip']}")

    print("\nMX Records:")
    for mx in results.get('mx_records', []):
        print(f"  {mx['mx_record']} -> {mx['ip']}")

    print("\nNS Records:")
    for ns in results.get('ns_records', []):
        print(f"  {ns['ns_record']} -> {ns['ip']}")

    print("\nTXT Records:")
    for txt in results.get('txt_records', []):
        print(f"  {txt}")
else:
    print("No results found or query failed.")
```

---

### 📋 Quick subdomain and IP extraction:

```python
ips, subdomains = client.get_simple_list("example.com")
print("Subdomains:")
for sub in subdomains:
    print(f"  {sub}")

print("IPs:")
for ip in ips:
    print(f"  {ip}")
```

---

## Notes

- `query_domain()` returns a dictionary with DNS data.
- Keys include: `a_records`, `mx_records`, `ns_records`, `txt_records`, and `ips_and_subdomains`.
- `get_simple_list()` returns two lists: all IPs and all subdomains found.

