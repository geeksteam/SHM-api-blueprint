import json
import time
import dredd_hooks as hooks

# Local vars
#

# Timer before requests object
requests_timer = {}

# Timer before all requests in GROUP object
groups_timer = {}

## Groups timers
groups_timer['Web Domains'] = 1

## Request timers
requests_timer['User Backups > List backups > List backups'] = 15
requests_timer['User Backups > Delete backup > Delete backup'] = 15

requests_timer['User Backups testing > Get all mysql users #User > Get all mysql users #User'] = 5
requests_timer['User Backups testing > Get all pgsql users #User > Get all pgsql users #User'] = 5
requests_timer['User Backups testing > Transfer backup to remote server > Transfer backup to remote server'] = 10
requests_timer['User Backups testing > Add mysql user #User > Add mysql user #User'] = 10
requests_timer['User Backups Restore testing > List all web domains of #User > List all web domains of #User'] = 10

requests_timer['Plugins > Start Plugin task > Start Plugin task'] = 10

## Add request number before its name to identify test
add_request_number = True
request_number = 0

## Add group name
add_group_name = True

##############
#  Functions

# Execute TIMER BEFORE requests
@hooks.before_each
def add_request_timer(transaction):

        # Check for GROUP timers
        if transaction['origin']['resourceGroupName'] in groups_timer and transaction['skip'] != True:
                seconds = groups_timer[ transaction['origin']['resourceGroupName'] ]
                transaction['request']['headers']['Dredd-Timer-Before'] = str(seconds)
                time.sleep(seconds)

        # Check for requests
        if transaction['name'] in requests_timer and transaction['skip'] != True:
                seconds = requests_timer[transaction['name']]
                transaction['request']['headers']['Dredd-Timer-Before'] = str(seconds)
                time.sleep(seconds)
                
# Add NUMBER to request name and Timer info.
@hooks.before_each
def add_request_number_and_group(transaction):
        # Add Timer information
        if transaction['name'] in requests_timer:
                transaction['origin']['actionName'] = '( Timer:'+ str(requests_timer[transaction['name']]) + ') '+ transaction['origin']['actionName']

        if transaction['origin']['resourceGroupName'] in groups_timer:
                transaction['origin']['actionName'] = '( Timer:'+ str(groups_timer[ transaction['origin']['resourceGroupName'] ]) + ') '+ transaction['origin']['actionName']
        
        append = ''
        # Add request number
        if add_request_number:
                global request_number 
                request_number += 1
                append = append + '['+ str(request_number) + '] '
        # Add group name
        if add_group_name:
                append = append + '[' + transaction['origin']['resourceGroupName'] + '] '

        transaction['origin']['actionName'] = append + transaction['origin']['actionName']
