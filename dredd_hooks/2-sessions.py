import json
import time
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
        'User Backups',
    ]
    
# List of REQUESTS that must be run from USER
#
user_requests = [
	]

# Local stash
stash = {}

###
# Local functions
###

# Set Cookie for User 
def set_user_cookie(transaction):
        transaction['request']['headers']['Cookie'] = stash['user_sessID']
        transaction['request']['headers']['Dredd-User'] = 'RegularUser'
# Set Cookie for Root 
def set_root_cookie(transaction):
        transaction['request']['headers']['Cookie'] = stash['root_sessID']
        transaction['request']['headers']['Dredd-User'] = 'Root'
# Set Expected response for 500 Errors
def set_expected_error(transaction):
        transaction['expected']['statusCode'] = '500'
        transaction['expected']['headers'] = {}
        transaction['expected']['headers']['Content-Type'] = 'application/json'
        transaction['expected']['body'] = '{ "error": { "code":"", "text":""} }'
        transaction['expected']['schema'] = '{ "error": { "code":"", "text":""} }'

###
# Hook functions
###

## Retrieve ROOT sessionID on a login
@hooks.after('Create regularUser for tests > Auth as Root for testing user creation > Auth as Root for testing user creation')
def stash_root_session_id(transaction):
		stash['root_sessID'] = transaction['real']['headers']['set-cookie']
        
@hooks.after('Panel Authorization > Root login > Root login success')
def stash_root_session_id(transaction):
		stash['root_sessID'] = transaction['real']['headers']['set-cookie']

## Retrieve USER sessionID on a login
@hooks.after('Panel Authorization > User login > Login success')
def stash_user_session_id(transaction):
		stash['user_sessID'] = transaction['real']['headers']['set-cookie']

## Set the ROOT or USER session cookie in all requests
# if #User tag provided in request name or request in group or list 
# of user request it will handle with user cookie.    
@hooks.before_each
def add_session_cookie(transaction):
        if 'user_sessID' in stash:
                # Check is request GROUP in USERs list
                if transaction['origin']['resourceGroupName'] in user_group_requests:
                        set_user_cookie(transaction)
                        return
                # Check is request NAME in USERs list
                if transaction['name'] in user_requests:
                        set_user_cookie(transaction)
                        return
                # Check for USER hash tag in request name (eg.: #User).
                hashTag = '#user'
                if hashTag in transaction['name'].lower():
                        set_user_cookie(transaction)
                        return
        # Run it as ROOT by default
        if 'root_sessID' in stash:
                set_root_cookie(transaction)

# Add response expectation if #Error hash tag in request name
@hooks.before_each
def add_error_expectation(transaction):
        hashTag = '#error'
        if hashTag in transaction['name'].lower():
                set_expected_error(transaction)
