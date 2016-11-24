import sys
import ftplib
import dredd_hooks as hooks

# Test FTP login as created account
@hooks.after('FTP accounts > !Hook FTP account testing > !Hook FTP account testing')
def check_ftp_account(transaction):
		if transaction['skip'] != True:
				print >> sys.stderr, 'Test FTP accounts Hook Started'
				print >> sys.stderr, 'Test FTP accounts Hook Done'
		return
		