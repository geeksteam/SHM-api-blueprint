import time
import socket
import dns.resolver
import dredd_hooks as hooks

# Test DNS server response records
@hooks.before('DNS Domains > List Domains records > List Domains records')
def check_dns_records(transaction):
        if transaction['skip'] != True:
				# Set the DNS Server
                resolver = dns.resolver.Resolver()
                resolver.nameservers=[transaction['host']]
                dnsresult = resolver.query('testpdns.com', 'MX')
                if len(dnsresult) < 1:
                        transaction['fail'] = "DNS response from %s for testpdns.com MX has no records" % transaction['host']
                print "Result of checking domains:"
                for rdata in dnsresult:
                        print rdata.target
