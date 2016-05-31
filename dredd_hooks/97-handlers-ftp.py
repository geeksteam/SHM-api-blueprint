import ftplib
import time
import dredd_hooks as hooks

# Test FTP login as created account
@hooks.after('FTP accounts > List FTP accounts > List FTP accounts')
def check_ftp_account(transaction):
        if transaction['skip'] != True:
				try:
						ftp = ftplib.FTP(transaction['host'])
						ftp.login(transaction['request']['headers']['Dredd-User']+'_FTP1', 'FTPPassword')
						# List directory
						files = ftp.dir()
						# Upload file
						myfile = open('/bin/sh', 'r')
						final_file_name = 'test_bin_upload'
						ftp.storbinary('STOR '+ final_file_name, myfile)
				except ftplib.all_errors as e:
						transaction['fail'] = "FTP account test by Dredd/Python FTPclient. Error: %s" % e