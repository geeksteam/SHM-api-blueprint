from ftplib import FTP
import time
import dredd_hooks as hooks

# Test FTP login as created account
@hooks.before('FTP accounts > List FTP accounts > List FTP accounts')
def check_ftp_account(transaction):
				transaction['fail'] = "Cannot login to FTP account by test. Error:"
