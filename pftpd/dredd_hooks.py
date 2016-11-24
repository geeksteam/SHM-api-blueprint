import sys
import ftplib
import dredd_hooks as hooks

# Test FTP login as created account
@hooks.before('FTP accounts > Remove FTP accounts > Remove FTP accounts')
def check_ftp_account_test(transaction):
		if transaction['skip'] != True:
				print >> sys.stderr, 'Test FTP accounts Hook Started'
				print >> sys.stderr, 'Test FTP accounts Hook Done'
