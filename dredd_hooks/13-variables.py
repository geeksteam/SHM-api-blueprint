import json
import sys
import time
import dredd_hooks as hooks

## Local stash
# Testing Server IP
# server_ip='95.163.191.21' Get from transaction host

# Root user password
rootUserPassword='goodSHMpassword'
# regular User name and password
regularUser='regularUser'
regularUserPassword='hbv8g28ba23'

# Testing domain
testDomain='test9521.com'

# current date 2022-01-31
currDateYMD=time.strftime("%Y.%m.%d")
currDateDMY=time.strftime("%d.%m.%Y")

## Backup testing
backup_server_ip='95.163.191.21'

        
# Replace $VARS
@hooks.before_each
def set_variables(transaction):
            if transaction['skip'] != True:

                    server_ip = transaction['host']

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

                    transaction['request']['body'] = transaction['request']['body'].replace('$BACKUP_SERVER_IP', backup_server_ip)
                    transaction['expected']['body'] = transaction['expected']['body'].replace('$BACKUP_SERVER_IP', backup_server_ip)

                    # Set testing domainName
                    transaction['request']['headers']['Testing-domain'] = testDomain
                    transaction['request']['body'] = transaction['request']['body'].replace('$TESTING_DOMAIN', testDomain)
                    transaction['expected']['body'] = transaction['expected']['body'].replace('$TESTING_DOMAIN', testDomain)

                    