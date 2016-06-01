import time
import json
import dredd_hooks as hooks

# Run grab url function
def run_url():
        req = Request('http://test.com/phpjson.php')
        try:
                response = urlopen(req)
        except HTTPError as e:
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        except URLError as e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
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
                try:
                        j = json.loads(response)
                except:
                        transaction['fail'] = 'Cannot decode response to JSON. Response is: %s' % response
                        return
                if check_nginx_php_fpm(j) == False:
                        transaction['fail'] = 'Nginx PHP FPM test failed. Data is:'.join(j)
