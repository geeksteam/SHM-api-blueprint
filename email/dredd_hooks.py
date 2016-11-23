import smtplib
import imaplib
from email.mime.text import MIMEText

import sys
import os
import re
import time
import json

from email import parser

import time
import dredd_hooks as hooks

# Global settings
testboxemail =     'info@'
destination = 'max@geeks.team'

# USERNAME = testboxemail@server
PASSWORD = "infoPassword"

# Wait until pop3 test
wait_before_pop3 = 20


@hooks.before_validation('Email boxes > !Hooks > !Hook pop3/smtp testing')
def test_email(transaction):
        if transaction['skip'] != True:
                SMTPserver = transaction['request']['headers']['Testing-domain']

                print >> sys.stderr, 'Test Email Hook started %s' % SMTPserver

                testbox = testboxemail + SMTPserver
                message_text = 'This is a text email message from Dredd testing suite.'
                subject_recieve_test = 'SMTP e-mail Dredd RECIEVE test'
                subject_auth_test = 'SMTP e-mail Dredd send AUTH test'

                USERNAME = testbox
                
                # Test of server SMTP recieveing emails from Dredd	
                print >> sys.stderr, 'Sending email to %s using localhost' % testbox
                dreddsender = 'dredd-test@geeks.team'

                msg_fromDredd = MIMEText(message_text)
                msg_fromDredd['From'] = dreddsender
                msg_fromDredd['To'] = testbox
                msg_fromDredd['Subject'] = subject_recieve_test

                smtpObj = smtplib.SMTP('localhost')
                smtpObj.set_debuglevel(True)
                smtpObj.sendmail(dreddsender, [testbox], msg_fromDredd.as_string())         
                smtpObj.quit()
                        
                # Send email using SMTP AUTH
                print >> sys.stderr, 'Sending email to %s using %s' % (destination, SMTPserver)
                msg_fromTestBOX = MIMEText(message_text)
                msg_fromTestBOX['From'] = testbox
                msg_fromTestBOX['To'] = destination
                msg_fromTestBOX['Subject'] = subject_auth_test
                
                conn = smtplib.SMTP(SMTPserver)
                conn.set_debuglevel(True)
                
                conn.login(USERNAME, PASSWORD)
                conn.sendmail(testbox, [destination], msg_fromTestBOX.as_string())
                conn.quit()
                        

                # Wait until message is proccesed by exim
                print >> sys.stderr, 'Waiting for %s seconds' % wait_before_pop3
                time.sleep(wait_before_pop3)

                # Check IMAP message is in box
                print >> sys.stderr, 'Checking mails in %s using IMAP' % SMTPserver

                imaplib.Debug = 4
                mail = imaplib.IMAP4(SMTPserver)
                mail.login(USERNAME, PASSWORD)
                mail.select('INBOX')
                result, data = mail.search(None, '(HEADER Subject "'+ subject_recieve_test +'")')
                ## If no messages found
                if result != 'OK':
                        transaction["fail"] = 'No mails with subject %s found.' % subject_recieve_test
                        print >> sys.stderr, transaction["fail"]
                        mail.close()
                        return
                ## Delete message
                for num in data[0].split():
                        print >> sys.stderr, 'Deleting mail with NUM: %s' % num
                        mail.store(num, '+FLAGS', '\\Seen \\Deleted')
                mail.expunge()
                mail.close()
                mail.logout()

                # Set to success
                transaction['real']['statusCode'] = 299
                transaction['real']['body'] = ''
