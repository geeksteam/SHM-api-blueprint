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
                try:
                        dnsresult = resolver.query('testpdns.com', 'MX')
                except dns.resolver.NXDOMAIN:
                        transaction['fail'] = "DNS testing error: No such domain %s" % args.host
                        return
                except dns.resolver.Timeout:
                        transaction['fail'] = "DNS testing error: Timed out while resolving %s" % args.host
                        return
                except dns.exception.DNSException:
                        transaction['fail'] = "DNS testing error: Unhandled exception: %s" % dns.exception.DNSException
                        return
                if len(dnsresult) < 1:
                        transaction['fail'] = "DNS response from %s for testpdns.com MX has no records" % transaction['host']
                print "Result of checking domains:"
                for rdata in dnsresult:
                        print rdata.target
