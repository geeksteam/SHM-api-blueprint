import json
import sys
import requests
import time
import dredd_hooks as hooks

# Local stash
last_backup_name = 'noBackupFound'
 
# Set backup arch Name
@hooks.before('Nginx URL statistics > Get all domains statistics > Get all domains statistics')
def make_url_statistics(transaction):
            if transaction['skip'] != True:
                    link = "http://test.com/url_one"
                    f = requests.get(link)
                    link = "http://test.com/url_two"
                    f = requests.get(link)
                    link = "http://test.com/url_two"
                    f = requests.get(link)
                    link = "http://test.com/url_three"
                    f = requests.get(link)
                    link = "http://test.com/url_three"
                    f = requests.get(link)
                    link = "http://test.com/url_three"
                    f = requests.get(link)
                    # Wait for statistic flush to bucket
                    time.sleep(63)
                    