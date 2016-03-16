import json
import dredd_hooks as hooks

stash = {}

# Retrieve ROOT sessionID on a login
@hooks.after('Panel Authorization > Root login > Login success')
def stash_root_session_id(transaction):
        stash['root_sessID'] = transaction['real']['headers']['set-cookie']

# Retrieve USER sessionID on a login
@hooks.after('Panel Authorization > User login > Login success')
def stash_user_session_id(transaction):
        stash['user_sessID'] = transaction['real']['headers']['set-cookie']

# Set the ROOT session cookie in all requests
@hooks.before_each
def add_session_cookie(transaction):
        if 'root_sessID' in stash:
                transaction['request']['headers']['Cookie'] = stash['root_sessID']
