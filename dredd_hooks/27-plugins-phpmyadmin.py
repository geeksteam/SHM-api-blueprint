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
                phpmyadminURL = 'http://%s/phpmyadmin' % testDomain
                d = pq(url=phpmyadminURL)
                title = d('title').text()
                # Check for title
                if 'phpMyAdmin' not in title:
                        print title
                        transaction['fail'] = 'Error phpMyAdmin title not found'
