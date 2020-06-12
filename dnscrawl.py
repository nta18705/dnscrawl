#! /usr/bin/python3

# dnscrawl - iterates through a wordlist and applies the wordlist as a subdomain of the supplied TLD.
# Wordlist can include single terms (e.g. www) or combined terms (e.g. remote.secure)
# outputs a list of valid FQDNs

# Usage: dnscrawl.py [-w filename] [-o output_file] top_level_domain

# Default wordlist (if none is suplied):

import dns
import dns.resolver
import sys
import argparse

def process_wordlist(wordlist, tld):
    fqdn_list = []
    for line in wordlist:
        fqdn = line.rstrip() + "." + tld 
        try:
            a_answers = dns.resolver.query(fqdn, 'A')
            print ("A record for ", fqdn, ":")
            fqdn_list.append(fqdn)
            for ipval in a_answers:
                print('IP', ipval.to_text())
        except(dns.resolver.NXDOMAIN):
            print(fqdn, "  :     Not found")
        except(dns.exception.Timeout):
            print("Timed out on     ", fqdn)
    return fqdn_list

def get_cnames(fqdn_list):
    cname_list = {}
    for fqdn in fqdn_list:
        try:
            cname_list[fqdn] = []
            a_answers = dns.resolver.query(fqdn, 'CNAME')
            for cnameval in a_answers:
                print(fqdn, ": CNAME: ", cnameval)
                cname_list[fqdn].append(cnameval)
        except(dns.resolver.NoAnswer):
            print(fqdn, "  :     No answer")
        except(dns.exception.Timeout):
            print("Timed out on     ", fqdn)
    return cname_list

def write_output_file(fqdn_list, cname_list, output_file):
    for fqdn in fqdn_list:
        output_file.write(fqdn + "\n")
        if cname_list[fqdn]:
            output_file.write("+CNAMEs:\n")
            for cname in cname_list[fqdn]:
                output_file.write("     > " + str(cname) +"\n")
    

def main():
    parser = argparse.ArgumentParser(description="Iterates through a supplied or built-in wordlist to see if FQDNs exist in a TLD")
    parser.add_argument('--wordlist', type=argparse.FileType('r'), help="Provide a path to a wordlist file")
    parser.add_argument('--output', type=argparse.FileType('w'), help="Provide an output file")
    parser.add_argument('tld', help="Give the top level domain you would like to test")
    args = parser.parse_args()
    if args.wordlist:
        wordlist = args.wordlist
        print("Reading wordlist from:   ", wordlist.name)
    if args.output:
        output_file = args.output
        print("Writing output to:    ", output_file.name)
    tld = args.tld
    print("Analysing:   ", tld)
    
    valid_fqdns = process_wordlist(wordlist, tld)
    cname_list = get_cnames(valid_fqdns)
    write_output_file(valid_fqdns, cname_list, output_file)

    wordlist.close()
    output_file.close()

if __name__ == '__main__':
    main()