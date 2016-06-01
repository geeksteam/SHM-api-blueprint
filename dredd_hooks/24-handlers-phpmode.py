import time
import dredd_hooks as hooks

# Checking PHP mode
@hooks.after('FTP accounts > List FTP accounts > List FTP accounts')
def check_php_mode(transaction):
        if transaction['skip'] != True:

