dnscrawl.py

dnscrawl is a simple python3 script that takes in a wordlist file and a TLD and then scans for A records in the TLD based on the contents of the wordlist.  If a valid A record is found, then a CNAME search is done on the FQDN as well.

Requires the following packages:
- dns
- argparse

Usage: dnscrawl.py [-h] [--wordlist WORDLIST] [--output OUTPUT] tld
