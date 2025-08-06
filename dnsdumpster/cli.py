# cli.py

import sys
from dnsdumpster import DNSDumpsterClient

def main():
    if len(sys.argv) != 2:
        print("Usage: dnsdumpster <domain>")
        sys.exit(1)
    domain = sys.argv[1]
    client = DNSDumpsterClient()
    results = client.query_domain(domain)
    if results:
        print(results)  # or format nicely
    else:
        print("No results found")

if __name__ == "__main__":
    main()
