import sys
import os

import dredd_hooks as hooks

from pyquery import PyQuery as pq
from lxml import etree
import urllib

## Checking WordPress installer as grabbing page and check title

@hooks.before_validation('Plugin WordPress > !Hook test installation > !Hook test installation')
def test_roundcube_plugin(transaction):
        if transaction['skip'] != True:
                # Get Test domain
                testDomain = transaction['request']['headers']['Testing-domain']

                wordpressURL = 'http://%s/wordpress' % testDomain

                # Try to open url
                try:
                        d = pq(url=wordpressURL)
                except Exception, e:
                        # Cant open url
                        print 'Cannot open URL:'+wordpressURL+' because:'+str(e)
                        transaction['fail'] = 'Cannot open URL:'+wordpressURL+' because:'+str(e)
                        return

                title = d('title').text()
                # Check for title
                if 'WordPress' not in title:
                        print title
                        transaction['fail'] = 'Error WordPress title not found.'
                        return
                # Success
                transaction['real']['statusCode'] = 299
                transaction['real']['body'] = ''
