import urllib2
import time
import dredd_hooks as hooks

 
# Set backup arch Name
@hooks.before('Nginx URL statistics > Get all domains statistics > Get all domains statistics')
def make_url_statistics(transaction):
        if transaction['skip'] != True:
                response = urllib2.urlopen('http://test.com/url_one').read()
                response = urllib2.urlopen('http://test.com/url_two').read()
                response = urllib2.urlopen('http://test.com/url_three').read()
                # Wait for statistic flush to bucket
                time.sleep(63)