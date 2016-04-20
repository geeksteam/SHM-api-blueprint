from urllib2 import Request, urlopen, URLError, HTTPError
import time
import dredd_hooks as hooks

# Run grab url function
def run_url(urlname):
        req = Request(urlname)
        try:
                response = urlopen(req)
        except HTTPError as e:
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        except URLError as e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
 
# Create url statistics
@hooks.before('Nginx URL statistics > Get all domains statistics > Get all domains statistics')
def make_url_statistics(transaction):
        if transaction['skip'] != True:
                run_url('http://test.com/url_one')
                run_url('http://test.com/url_two')
                run_url('http://test.com/url_three')
                # Wait for statistic flush to bucket
                time.sleep(63)