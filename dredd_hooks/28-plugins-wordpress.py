import sys
import os

import dredd_hooks as hooks

from pyquery import PyQuery as pq
from lxml import etree
import urllib

## Checking WordPress installer as grabbing page and check title

@hooks.after('Plugin WordPress > Install Wordpress to domain dir as #User > Install Wordpress to domain dir as #User')
def test_roundcube_plugin(transaction):
        if transaction['skip'] != True:
                wordpressURL = 'http://%s/wordpress' % testDomain
                d = pq(url=wordpressURL)
                title = d('title').text()
                # Check for title
                if 'WordPress' not in title:
                        print title
                        transaction['fail'] = 'Error WordPress title not found.'
