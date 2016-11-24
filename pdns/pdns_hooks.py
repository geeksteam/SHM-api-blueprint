import time
import socket
import dredd_hooks as hooks

import dns.query
import dns.resolver
from dns.exception import DNSException

test_domain='testpdns.com'
record_type=dns.rdatatype.MX

# Test DNS server response records
@hooks.before_validation('DNS Domains > !Hook query DNS server for responses > !Hook query DNS server for responses')
def check_dns_records(transaction):
        if transaction['skip'] != True:
        
                transaction['request']['headers']['Dredd-Testing'] = 'DNS client testing domain %s type %s' % (test_domain, record_type)
                
                # Set the DNS Server MX record of domain            
                query = dns.message.make_query(test_domain, record_type)
                response = dns.query.udp(query, transaction['host'])
                rcode = response.rcode()
                
                if rcode != dns.rcode.NOERROR:
                        if rcode == dns.rcode.NXDOMAIN:
                                transaction['fail'] = "DNS testing error: No such domain"
                                return
                        else:
                                transaction['fail'] = "DNS testing error: %s" % (dns.rcode.to_text(rcode))
                                return

                rrsets = response.answer
                if len(rrsets) < 1:
                        transaction['fail'] = "DNS testing error: Empty records set got from NS server."
                        return
                if rrsets[0][0].rdtype != dns.rdatatype.MX:
                        transaction['fail'] = "DNS testing error: No MX record found"
                        return
                # Success
                transaction['real']['statusCode'] = 299
                transaction['real']['body'] = ''
                