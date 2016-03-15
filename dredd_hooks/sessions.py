import json
import dredd_hooks as hooks

stash = {}

# hook to retrieve session on a login
@hooks.after('Panel Authorization > User login > Login success')
def stash_session_id(transaction):
	parsed_body = json.loads(transaction['real']['body'])
	stash['token'] = parsed_body['sessionID']

# hook to set the session cookie in all following requests
@hooks.before_each
def add_session_cookie(transaction):
	if 'token' not in stash:
		transaction['request']['headers']['Cookie'] = "sessionID=" + stash['token']
		