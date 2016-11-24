import sys
import os

import dredd_hooks as hooks

from pyquery import PyQuery as pq
from lxml import etree
import urllib

## Checking RoundCube webmail as grabbing page and check title

@hooks.before_validation('Plugin Roundcube > Add RoundCube WebMail to domain as #User > !Hook test installation')
def test_roundcube_plugin(transaction):
        if transaction['skip'] != True:
                # Get Test domain
                testDomain = transaction['request']['headers']['Testing-domain']

                roundcubeURL = 'http://%s/roundcube' % transaction['request']['headers']['Testing-domain']
                # Try to open url
                try:
                        d = pq(url=roundcubeURL)
                except Exception, e:
                        # Cant open url
                        print 'Cannot open URL:'+roundcubeURL+' because:'+str(e)
                        transaction['fail'] = 'Cannot open URL:'+roundcubeURL+' because:'+str(e)
                        return

                title = d('title').text()
                message = d('div#message').text()
                # Check for title
                if 'Roundcube Webmail' not in title:
                        print title
                        transaction['fail'] = 'Error RoundCube title not found'
                        return
                # Check for error message
                if message != '':
                        print message
                        transaction['fail'] = 'Error message in RoundCube not empty'
                        return
                # Success
                transaction['real']['statusCode'] = 299
                transaction['real']['body'] = ''
