import ftplib
import time
import dredd_hooks as hooks

# Test FTP login as created account
@hooks.after('FTP accounts > List FTP accounts > List FTP accounts')
def check_ftp_account(transaction):
        if transaction['skip'] != True:
		
				transaction['request']['headers']['Dredd-Testing'] = 'FTP Client testing as user %s' % (transaction['request']['headers']['Dredd-User']+'_FTP1')
				
				try:
						ftp = ftplib.FTP(transaction['host'])
						ftp.login(transaction['request']['headers']['Dredd-User']+'_FTP1', 'FTPPassword')
						# List directory
						files = ftp.dir()
						# Upload file
						myfile = open('/var/www/html/phpjson.php', 'r')
						final_file_name = 'phpjson.php'
						ftp.storbinary('STOR '+ final_file_name, myfile)
				except ftplib.all_errors as e:
						transaction['fail'] = "FTP account test by Dredd/Python FTPclient. Error: %s" % e
