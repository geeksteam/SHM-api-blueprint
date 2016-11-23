import smtplib
import poplib, email
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
PASSWORD = "infoPasswordj"

# Wait until pop3 test
wait_before_pop3 = 15


@hooks.before_validation('Email boxes > !Hooks > !Hook pop3/smtp testing')
def test_email(transaction):
        if transaction['skip'] != True:
                SMTPserver = transaction['request']['headers']['Testing-domain']

                print >> sys.stderr, 'Test Email Hook started %s' % SMTPserver

                testbox = testboxemail + SMTPserver

                USERNAME = testbox
                
                # Test of server SMTP recieveing emails from Dredd	
                print >> sys.stderr, 'Sending email to %s' % testbox
                dreddsender = 'dredd-test@geeks.team'

                msg_fromDredd = MIMEText('This is a text email message from Dredd testing suite.')
                msg_fromDredd['From'] = dreddsender
                msg_fromDredd['To'] = testbox
                msg_fromDredd['Subject'] = 'SMTP e-mail Dredd RECIEVE test'

                smtpObj = smtplib.SMTP('localhost')
                smtpObj.set_debuglevel(True)
                smtpObj.sendmail(dreddsender, [testbox], msg_fromDredd.as_string())         
                smtpObj.quit()
                        
                # Send email using SMTP AUTH
                print >> sys.stderr, 'Sending email to %s' % destination
                msg_fromTestBOX = MIMEText('This is a text email message from Dredd testing suite.')
                msg_fromTestBOX['From'] = testbox
                msg_fromTestBOX['To'] = destination
                msg_fromTestBOX['Subject'] = 'SMTP e-mail Dredd send AUTH test'
                
                conn = smtplib.SMTP(SMTPserver)
                conn.set_debuglevel(True)
                
                conn.login(USERNAME, PASSWORD)
                conn.sendmail(testbox, [destination], msg_fromTestBOX.as_string())
                conn.quit()
                        

                # Wait until message is proccesed by exim
                print >> sys.stderr, 'Waiting for %s seconds' % wait_before_pop3
                time.sleep(wait_before_pop3)

                # Check POP3 message is in box
                print >> sys.stderr, 'Checking mails in %s using POP3' % SMTPserver

                box = poplib.POP3(SMTPserver)
                box.set_debuglevel(True)
                box.user(USERNAME)
                box.pass_(PASSWORD)

                #Get messages from server:
                messages = [box.retr(i) for i in range(1, len(box.list()[1]) + 1)]
                # Concat message pieces:
                messages = ["\n".join(mssg[1]) for mssg in messages]
                #Parse message intom an email object:
                messages = [parser.Parser().parsestr(mssg) for mssg in messages]
                
                print >> sys.stderr, 'Mail found: %s' % len(messages)

                message_found = False
                i=0
                for message in messages:
                        i=i+1
                        print >> sys.stderr, 'Found Mail: %s' % message['from']
                        # Check for message from Dredd
                        if 'dredd-test@geeks.team' in message['from'] :
                                print >> sys.stderr, 'Mail from DREDD found: %s' % message['from']
                                message_found = True
                        # Delete message
                        box.dele(i)
                box.quit()
                
                if message_found == False:
                        transaction["fail"] = "Dredd POP3 client failed: Message from DREDD not found in messages list. Total messages: %s" % i
                        return
                # Set to success
                transaction['real']['statusCode'] = 299
                transaction['real']['body'] = ''
