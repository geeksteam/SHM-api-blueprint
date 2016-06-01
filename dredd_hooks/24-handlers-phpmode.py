import time
import json
from urllib2 import Request, urlopen, URLError, HTTPError
import dredd_hooks as hooks

# Url where is phpjson is
phpjson_url='http://test.com/phpjson.php'

# Run grab url function
def run_url():
        req = Request(phpjson_url)
        try:
                response = urlopen(req)
        except HTTPError as e:
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
                return False
        except URLError as e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
                return False
        return response

# Check for nginx PHP FPM
def check_nginx_php_fpm(j):
        if j['SAPI'] != 'fpm-fcgi':
                return False
        if "nginx" not in j['Server']: 
                return False

# Checking PHP mode
@hooks.before('Web Domains > List all web domains > List web domains')
def check_php_mode(transaction):
        if transaction['skip'] != True:
        
                response = run_url()        
                if response == False:
                        transaction['fail'] = 'Cennot get test URL %s' % phpjson_url
                        return
                try:
                        j = json.loads(response)
                except:
                        transaction['fail'] = 'Cannot decode response to JSON. Response is: %s' % response
                        return
                if check_nginx_php_fpm(j) == False:
                        transaction['fail'] = 'Nginx PHP FPM test failed. Data is:'.join(j)
