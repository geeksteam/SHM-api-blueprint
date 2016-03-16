import json
import dredd_hooks as hooks

stash = {}

# List of requests from USER not root
user_requests = [
		'User defined settings > /api/user/password > POST'
	]


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
	# Check is transaction in user list
	if transaction['name'] in user_requests:
        if 'user_sessID' in stash:
                transaction['request']['headers']['Cookie'] = stash['user_sessID']
    # run it as root
    else:
    	if 'root_sessID' in stash:
                transaction['request']['headers']['Cookie'] = stash['root_sessID']
