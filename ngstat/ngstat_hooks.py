from urllib2 import Request, urlopen, URLError, HTTPError
import time
import dredd_hooks as hooks
from subprocess import Popen, PIPE

# Run grab url function
def open_ngstat_url(urlname):
        req = Request(urlname)
        response = urlopen(req).read()
        return True

# Create url statistics
@hooks.before_validation('Domains statistics > !Hooks > !Hook to simulate get urls')
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

                open_ngstat_url('http://%s/path1/index.html' % testDomain)
                time.sleep(1)
                open_ngstat_url('http://%s/path2/index.html' % testDomain)
                time.sleep(1)
                open_ngstat_url('http://%s/path2/index.html' % testDomain)
                time.sleep(1)
                open_ngstat_url('http://%s/path2/index.html' % testDomain)
                # Wait for statistic flush to bucket
                time.sleep(60)
                # Set to success
                transaction['real']['statusCode'] = 299
                transaction['real']['body'] = ''
