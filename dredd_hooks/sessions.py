import json
import dredd_hooks as hooks

stash = {}

# List of groups that must be run as USER
user_group_requests = [
        'User defined settings',
    ]

# List of requests that must be run from USER
user_requests = []


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
    # Check is request GROUP in USER list
    if transaction['origin']['resourceGroupName'] in user_group_requests and 'user_sessID' in stash:
        transaction['request']['headers']['Cookie'] = stash['user_sessID']
        return

	# Check is request in USER list
	if transaction['name'] in user_requests and 'user_sessID' in stash:
        transaction['request']['headers']['Cookie'] = stash['user_sessID']
        return

    # run it as ROOT by default
    if 'root_sessID' in stash:
        transaction['request']['headers']['Cookie'] = stash['root_sessID']