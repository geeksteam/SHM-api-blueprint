import ftplib
import time
import dredd_hooks as hooks

# Test FTP login as created account
@hooks.after('FTP accounts > List FTP accounts > List FTP accounts')
def check_ftp_account(transaction):
        if transaction['skip'] != True:
				try:
						ftp = ftplib.FTP(transaction['host'])
						ftp.login('FTP1', 'FTPPassword')
						files = ftp.dir()
				except ftplib.all_errors as e:
						transaction['fail'] = True
						transaction['real']['body'] = "Cannot login to FTP account by test. Error: %s" % e
