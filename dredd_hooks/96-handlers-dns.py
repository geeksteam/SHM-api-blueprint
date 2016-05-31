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
                        dnsresult = resolver.query.udp('testpdns.com', 'MX')
                except dns.resolver.NXDOMAIN:
                        transaction['fail'] = "DNS testing error: No such domain"
                        return
                except dns.resolver.NoAnswer:
                        transaction['fail'] = "DNS testing error: No answer from dns %s" % transaction['host']
                        return
                except dns.resolver.Timeout:
                        transaction['fail'] = "DNS testing error: Timed out while resolving %s" % transaction['host']
                        return
                except dns.exception.DNSException as e:
                        transaction['fail'] = "DNS testing error: Unhandled exception: %s" % e.message
                        return
                if len(dnsresult) < 1:
                        transaction['fail'] = "DNS response from %s for testpdns.com MX has no records" % transaction['host']
                print "Result of checking domains:"
                for rdata in dnsresult:
                        print rdata.target
