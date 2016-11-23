import json
import sys
import time
import dredd_hooks as hooks

## Local stash
# Testing Server IP

# variables
variables = {}
# Root user password
variables['$ROOT_PASSWORD']='goodSHMpassword'
# regular User name and password
variables['$USER_NAME']='regularUser'
variables['$USER_PASSWORD']='hbv8g28ba23'
# Testing domain
variables['$TESTING_DOMAIN']='9521.geeks.team'
# current date 2022-01-31
variables['$DATE_YMD']=time.strftime("%Y.%m.%d")
variables['$DATE_DMY']=time.strftime("%d.%m.%Y")
# Backup testing
variables['$BACKUP_SERVER_IP']='95.163.191.21'
# Slack plugins token test
variables['$SLACK_TOKEN'] = "xoxb" + "-" + "56128066644-DFy3Bcry4RnFKRHmJZGt9aD8"


# Replace $VARS
@hooks.before_each
def set_variables(transaction):
	if transaction['skip'] != True:
		print >> sys.stderr, 'Replace Variables HOOK'

		# Set testing domainName
		transaction['request']['headers']['Testing-domain'] = variables['$TESTING_DOMAIN']
		# Add server_ip
		variables['$SERVER_IP'] = transaction['host']

		# Iterate over keys
		for key, value in variables.iteritems():
			transaction['request']['body'] = transaction['request']['body'].replace(key, value)
			transaction['expected']['body'] = transaction['expected']['body'].replace(key, value)
