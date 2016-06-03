import json
import time
import dredd_hooks as hooks

# Local vars
#
requests_timer = {}
requests_timer['User Backups > List backups > List backups'] = 15
requests_timer['User Backups > Delete backup > Delete backup'] = 15

requests_timer['User Backups testing > Get all mysql users #User > Get all mysql users #User'] = 5
requests_timer['User Backups testing > Get all pgsql users #User > Get all pgsql users #User'] = 5
requests_timer['User Backups testing > Transfer backup to remote server > Transfer backup to remote server'] = 10
requests_timer['User Backups testing > Add mysql user #User > Add mysql user #User'] = 10
requests_timer['User Backups Restore testing > List all web domains of #User > List all web domains of #User'] = 10

# Add request number before its name to identify test
add_request_number = True
request_number = 0

# Execute TIMER BEFORE requests
@hooks.before_each
def add_request_timer(transaction):
        # Sleep
        if transaction['name'] in requests_timer and transaction['skip'] != True:
                seconds = requests_timer[transaction['name']]
                transaction['request']['headers']['Dredd-Timer-Before'] = str(seconds)
                time.sleep(seconds)
                
# Add NUMBER to request name and Timer info.
@hooks.before_each
def add_request_number(transaction):
        # Add Timer information
        if transaction['name'] in requests_timer:
                transaction['origin']['actionName'] = '( Timer:'+ str(requests_timer[transaction['name']]) + ') '+ transaction['origin']['actionName']
        # Iterate request number
        if add_request_number:
                global request_number 
                request_number += 1
                transaction['origin']['actionName'] = '['+ str(request_number) + '] '+ transaction['origin']['actionName']