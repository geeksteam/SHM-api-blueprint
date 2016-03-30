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
        'DNS Domains',
        'FTP accounts',
        'Email boxes',
        'DKIM',
    ]
# List of REQUESTS that must be run from USER
#
user_requests = [
		'Sessions > Session information > Regular user',
		'Sessions > Domains list > User domains list',
		'Cron > Setting Job for restricted user > Setting Job for restricted user',
        'Filemanager > Create new directory > Make dir by User',
        'Filemanager > List directory > List dir by User',
        'Filemanager > List directory > List dir Error',
        'Filemanager > Change permissions > Change permissions by User',
        'Filemanager > Change permissions > Change permissions Error',
        'Filemanager > Change permissions > Change permissions while file Not Exist',
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
                # Check is request GROUP in USERs list
                if transaction['origin']['resourceGroupName'] in user_group_requests:
                        transaction['request']['headers']['Cookie'] = stash['user_sessID']
                        transaction['request']['headers']['User'] = 'RegularUser'
                        return
                # Check is request NAME in USERs list
                if transaction['name'] in user_requests:
                        transaction['request']['headers']['Cookie'] = stash['user_sessID']
                        transaction['request']['headers']['User'] = 'RegularUser'
                        return
                # Check for USER hash tag in request name (eg.: #User).
                hashTag = '#user'
                requestName = transaction['name'].lower()
                if hashTag in requestName:
                        transaction['request']['headers']['Cookie'] = stash['user_sessID']
                        transaction['request']['headers']['User'] = 'RegularUser'
                        return
                # Run it as ROOT by default
                if 'root_sessID' in stash:
                        transaction['request']['headers']['Cookie'] = stash['root_sessID']
                        transaction['request']['headers']['User'] = 'Root'

# Add response expectation if #Error hash tag in request name
@hooks.before_each
def add_error_expectation(transaction):
        hashTag = '#error'
        requestName = transaction['name'].lower()
        if hashTag in requestName:
                transaction['expected']['statusCode'] = '500'
                transaction['expected']['headers']['Content-Type'] == 'application/json':
                transaction['expected']['schema'] = '{ "error": { "code":"", "text":""} }'
