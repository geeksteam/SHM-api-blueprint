# -*- coding: utf-8 -*-

import time
import json
import urllib2
import dredd_hooks as hooks

# Url where is phpjson is
userName='regularUser'

# Run grab url function
def open_phpjson_url(phpjson_url):

        req = urllib2.Request(phpjson_url)
        response = urllib2.urlopen(req)
        out = response.read()

        return out

# Check for nginx PHP FPM
def check_nginx_php_fpm(j):
        if j['SAPI'] != 'fpm-fcgi':
                return False
        if "nginx" not in j['Server']: 
                return False
        if j['User'] != userName:
                return False
                
# Check for apache PHP FPM
def check_apache_php_fpm(j):
        if j['SAPI'] != 'fpm-fcgi':
                return False
        if "Apache" not in j['Server']: 
                return False
        if j['User'] != userName:
                return False

# Check for apache mod_php
def check_apache_mod_php(j):
        if j['SAPI'] != 'apache2handler':
                return False
        if "Apache" not in j['Server']: 
                return False

# Checking PHP mode
@hooks.after('Web Domains > PHP modes > PHP-FPM on Nginx')
def check_php_mode_PHP_FPM_NGINX(transaction):
        if transaction['skip'] != True:
                phpjson_url='http://%s/phpjson.php' % transaction['request']['headers']['Testing-domain']
                response = open_phpjson_url(phpjson_url)

                try:
                        j = json.loads(response)
                except:
                        transaction['fail'] = 'Cannot decode response from %s to JSON. Response is: %s' % (phpjson_url, response)
                        return
                if check_nginx_php_fpm(j) == False:
                        transaction['fail'] = 'Nginx PHP FPM mode check failed. Data is:'.join(j)
                        
@hooks.after('Web Domains > PHP modes > PHP-FPM on Apache')
def check_php_mode_PHP_FPM_APACHE(transaction):
        if transaction['skip'] != True:
                phpjson_url='http://%s/phpjson.php' % transaction['request']['headers']['Testing-domain']
                response = run_url(phpjson_url)        
                if response == False:
                        transaction['fail'] = 'Cannot get test URL %s' % phpjson_url
                        return
                try:
                        j = json.loads(response)
                except:
                        transaction['fail'] = 'Cannot decode response to JSON. Response is: %s' % response
                        return
                if check_apache_php_fpm(j) == False:
                        transaction['fail'] = 'Apache PHP FPM mode check failed. Data is:'.join(j)
                        
@hooks.after('Web Domains > PHP modes > Apache mod_php')
def check_php_mode_MOD_PHP(transaction):
        if transaction['skip'] != True:
                phpjson_url='http://%s/phpjson.php' % transaction['request']['headers']['Testing-domain']
                response = run_url(phpjson_url)        
                if response == False:
                        transaction['fail'] = 'Cannot get test URL %s' % phpjson_url
                        return
                try:
                        j = json.loads(response)
                except:
                        transaction['fail'] = 'Cannot decode response to JSON. Response is: %s' % response
                        return
                if check_apache_mod_php(j) == False:
                        transaction['fail'] = 'Apache mod_php mode check failed. Data is:'.join(j)

@hooks.after('Web Domains > PHP modes > PHP off')
def check_php_mode_PHP_OFF(transaction):
        if transaction['skip'] != True:
                phpjson_url='http://%s/phpjson.php' % transaction['request']['headers']['Testing-domain']
                response = run_url(phpjson_url)        
                if response == False:
                        transaction['fail'] = 'Cannot get test URL %s' % phpjson_url
                        return
                if response is None:
                        transaction['fail'] = 'Test URL %s is empty' % phpjson_url
                        return
                if '<?php' not in response:
                        transaction["fail"] = "Apache PHP off mode failed. Data is: %s " % response
