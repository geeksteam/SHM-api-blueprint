import sys
import os

import dredd_hooks as hooks

from pyquery import PyQuery as pq
from lxml import etree
import urllib

## Checking RoundCube webmail as grabbing page and check title

@hooks.after('Plugin Roundcube > Add RoundCube WebMail to domain as #User > Add RoundCube WebMail to domain as #User')
def test_roundcube_plugin(transaction):
        if transaction['skip'] != True:
                # Get Test domain
                testDomain = transaction['request']['headers']['Testing-domain']

                roundcubeURL = 'http://%s/roundcube' % testDomain
                d = pq(url=roundcubeURL)
                title = d('title').text()
                message = d('div#message').text()
                # Check for title
                if 'Roundcube Webmail' not in title:
                        print title
                        transaction['fail'] = 'Error RoundCube title not found'
                # Check for error message
                if message != '':
                        print message
                        transaction['fail'] = 'Error message in RoundCube not empty'
