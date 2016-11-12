from urllib2 import Request, urlopen, URLError, HTTPError
import time
import dredd_hooks as hooks
from subprocess import Popen, PIPE

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
                # Check IP and test.com in /etc/hosts
                process = Popen(["grep","-q",transaction['host'],"/etc/hosts"], stdout=PIPE)
                process.communicate()    # execute it, the output goes to the stdout
                exit_code = process.wait()    # when finished, get the exit code
                if exit_code > 0:
                        transaction['fail'] = "Python http client check by Dredd/Python error: Cannot find IP %s test.com in /etc/hosts" % transaction['host']
                # Run server requests
                testDomain = transaction['request']['headers']['Testing-domain']

                run_url('http://%s/url_one' % testDomain)

                run_url('http://%s/url_two' % testDomain)
                time.sleep(1)
                run_url('http://%s/url_two' % testDomain)
                time.sleep(1)
                run_url('http://%s/url_two' % testDomain)
                time.sleep(1)
                run_url('http://%s/url_three' % testDomain)
                # Wait for statistic flush to bucket
                time.sleep(65)
                