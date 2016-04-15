import json
import sys
import dredd_hooks as hooks

# Local stash
server_ip='95.163.191.20'

        
# Replace $SERVER_IP by real ip
@hooks.before_each
def set_server_ip(transaction):
            if transaction['skip'] != True:
                    transaction['request']['body'] = transaction['request']['body'].replace('$SERVER_IP', server_ip)
