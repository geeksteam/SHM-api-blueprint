import json
import dredd_hooks as hooks

stash = {}

# hook to retrieve session on a login
@hooks.after('Panel Authorization > User login > Login success')
def stash_session_id(transaction):
	stash['sessCookie'] = transaction['real']['headers']['set-cookie']

# hook to set the session cookie in all following requests
@hooks.before_each
def add_session_cookie(transaction):
	if 'sessCookie' not in stash:
		transaction['request']['headers']['Cookie'] = stash['sessCookie']
		