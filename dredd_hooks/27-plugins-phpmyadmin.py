import sys
import os

import dredd_hooks as hooks

from pyquery import PyQuery as pq
from lxml import etree
import urllib

## Checking PhpMyAdmin as grabbing page and check title

@hooks.after('Plugin PhpMyAdmin > Add pmainstall to domain as #User > Add pmainstall to domain as #User')
def test_roundcube_plugin(transaction):
        if transaction['skip'] != True:
                # Get Test domain
                testDomain = transaction['request']['headers']['Testing-domain']

                phpmyadminURL = 'http://%s/phpmyadmin' % testDomain

                # Try to open url
                try:
                        d = pq(url=phpmyadminURL)
                except Exception, e:
                        # Cant open url
                        print 'Cannot open URL:'+phpmyadminURL+' because:'+str(e)
                        transaction['fail'] = 'Cannot open URL:'+phpmyadminURL+' because:'+str(e)
        
                title = d('title').text()
                # Check for title
                if 'phpMyAdmin' not in title:
                        print title
                        transaction['fail'] = 'Error phpMyAdmin title not found'
