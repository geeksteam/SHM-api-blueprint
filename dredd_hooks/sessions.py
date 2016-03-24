import json
import dredd_hooks as hooks

###
# Requests and groups of requests listed below in arrays will run as regular USER by adding sessinID in requests headers,
# which catch and save to stash during user login testing.
# All requests which not listed here will run as ROOT user.
###

# List of GROUP that must be run as USER
#
user_group_requests = [
        'User defined settings',
        'SSL Certificates',
        'Web Domains',
        'MySQL Users',
        'MySQL Databases',
        'PgSQL Users',
        'PgSQL Databases',
        'FTP accounts',
        'Email boxes',
        'DKIM',
    ]
# List of REQUESTS that must be run from USER
#
user_requests = [
		'Sessions > Session information > Regular user',
		'Sessions > Domains list > User domains list',
		'Logout > User logout > User logout',
	]
# Local stash
stash = {}


###
# Hook functions
###

# Retrieve ROOT sessionID on a login
@hooks.after('Panel Authorization > Root login > Root login success')
def stash_root_session_id(transaction):
		stash['root_sessID'] = transaction['real']['headers']['set-cookie']

# Retrieve USER sessionID on a login
@hooks.after('Panel Authorization > User login > Login success')
def stash_user_session_id(transaction):
		stash['user_sessID'] = transaction['real']['headers']['set-cookie']


# Set the ROOT or USER session cookie in all requests
@hooks.before_each
def add_session_cookie(transaction):
	
	if 'user_sessID' in stash:
		# Check is request GROUP in USER list
		if transaction['origin']['resourceGroupName'] in user_group_requests:
				transaction['request']['headers']['Cookie'] = stash['user_sessID']
				transaction['request']['headers']['User'] = 'RegularUser'
				return
		# Check is request in USER list
		if transaction['name'] in user_requests:
				transaction['request']['headers']['Cookie'] = stash['user_sessID']
				transaction['request']['headers']['User'] = 'RegularUser'
				return

	# run it as ROOT by default
	if 'root_sessID' in stash:
			transaction['request']['headers']['Cookie'] = stash['root_sessID']
			transaction['request']['headers']['User'] = 'Root'