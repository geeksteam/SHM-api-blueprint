import time
import socket
import dredd_hooks as hooks

import dns.query
import dns.resolver
from dns.exception import DNSException

# Test DNS server response records
@hooks.before('DNS Domains > List Domains records > List Domains records')
def check_dns_records(transaction):
        if transaction['skip'] != True:
        
                # Set the DNS Server                
                query = dns.message.make_query("testpdns.com", dns.rdatatype.MX)
                response = dns.query.udp(query, transaction['host'])
                if rcode != dns.rcode.NOERROR:
                        if rcode == dns.rcode.NXDOMAIN:
                                transaction['fail'] = "DNS testing error: No such domain"
                                return
                        else:
                                transaction['fail'] = "DNS testing error: %s" % (dns.rcode.to_text(rcode))
                                return
                rrsets = response.answer
                if len(rrsets) < 1:
                        transaction['fail'] = "Empty records set got from NS"
                        return
                if rrsets[0][0].rdtype != dns.rdatatype.MX:
                        transaction['fail'] = "No MX record found"
                        return