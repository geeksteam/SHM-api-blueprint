import json
import sys
import time
import dredd_hooks as hooks

## Local stash
# Testing Server IP
server_ip='95.163.191.20'
# Root user password
rootUserPassword='goodSHMpassword'
# regular User name and password
regularUser='regularUser'
regularUserPassword='hbv8g28ba23'
# current date 2022-01-31
currDateYMD=time.strftime("%Y-%m-%d")
currDateDMY=time.strftime("%d.%m.%Y")
        
# Replace $SERVER_IP by real ip
@hooks.before_each
def set_variables(transaction):
            if transaction['skip'] != True:
                    transaction['request']['body'] = transaction['request']['body'].replace('$SERVER_IP', server_ip)
                    transaction['expected']['body'] = transaction['expected']['body'].replace('$SERVER_IP', server_ip)
                    
                    transaction['request']['body'] = transaction['request']['body'].replace('$ROOT_PASSWORD', rootUserPassword)
                    transaction['expected']['body'] = transaction['expected']['body'].replace('$ROOT_PASSWORD', rootUserPassword)
                    
                    transaction['request']['body'] = transaction['request']['body'].replace('$USER_NAME', regularUser)
                    transaction['expected']['body'] = transaction['expected']['body'].replace('$USER_NAME', regularUser)
                    
                    transaction['request']['body'] = transaction['request']['body'].replace('$USER_PASSWORD', regularUserPassword)
                    transaction['expected']['body'] = transaction['expected']['body'].replace('$USER_PASSWORD', regularUserPassword)
                    
                    transaction['request']['body'] = transaction['request']['body'].replace('$DATE_YMD', currDateYMD)
                    transaction['expected']['body'] = transaction['expected']['body'].replace('$DATE_YMD', currDateYMD)
                    
                    transaction['request']['body'] = transaction['request']['body'].replace('$DATE_DMY', currDateDMY)
                    transaction['expected']['body'] = transaction['expected']['body'].replace('$DATE_DMY', currDateDMY)
                    