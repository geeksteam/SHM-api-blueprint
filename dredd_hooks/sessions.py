import json
import dredd_hooks as hooks

stash = {}

# hook to retrieve session on a login
@hooks.after('Panel Authorization > User login > Login success')
def stash_session_id(transaction):
        stash['sessID'] = 'sessionID=kgekgTeGyRBrqXPnSjtWXVtu'
        #stash['sessID'] = transaction['real']['headers']['set-cookie']

# hook to set the session cookie in all following requests
@hooks.before_each
def add_session_cookie(transaction):
        if 'sessID' in stash:
                transaction['request']['headers']['Cookie'] = stash['sessID']
