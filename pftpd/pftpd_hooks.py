import sys
import ftplib
import dredd_hooks as hooks

# Test FTP login as created account
@hooks.before('FTP accounts > Remove FTP accounts > Remove FTP accounts')
def check_ftp_account_test(transaction):
		if transaction['skip'] != True:
				print >> sys.stderr, 'Test FTP accounts Hook Started'

				ftp = ftplib.FTP(transaction['host'])
				ftp.login(transaction['request']['headers']['Dredd-User']+'_FTP1', 'FTPPassword')
				
				# Upload phpjson.php file
				myfile = open('/var/www/html/phpjson.php', 'r')
				final_file_name = 'phpjson.php'
				ftp.storbinary('STOR '+ final_file_name, myfile)

				# Upload index.html to path1 path2
				myfile = open('/var/www/html/index.html', 'r')
				final_file_name = 'index.html'

				# go in and store
				try:
						ftp.rmd('/path1')
				except:
						pass
				ftp.mkd('/path1')
				ftp.cwd('/path1')
				ftp.storbinary('STOR '+ final_file_name, myfile)
				
				# go in and store
				try:
						ftp.rmd('/path2')
				except:
						pass
				ftp.mkd('/path2')
				ftp.cwd('/path2')
				ftp.storbinary('STOR '+ final_file_name, myfile)
				# Set to success
				transaction['real']['statusCode'] = 299
				transaction['real']['body'] = ''
				print >> sys.stderr, 'Test FTP accounts Hook Done'
