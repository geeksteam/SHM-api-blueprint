import json
import dredd_hooks as hooks

stash = {}

# hook to retrieve session on a login
@hooks.after('Panel Authorization > Login success > POST')
def stash_session_id(transaction):

	parsed_body = json.loads(transaction['real']['body'])
	stash['token'] = parsed_body['sessionID']
	print 'Session hook'

# hook to set the session cookie in all following requests
@hooks.before_each
def add_session_cookie(transaction):
	print 'After each'
	if 'token' not in stash:
		transaction['request']['headers']['Cookie'] = "sessionID=" + stash['token']
		