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
PASSWORD = "infoPassword"

# Wait until pop3 test
wait_before_pop3 = 15


@hooks.before_validation('Email boxes > Hook pop3/smtp testing > Hook pop3/smtp testing')
def test_email(transaction):
        if transaction['skip'] != True:
                print >> sys.stderr, 'Test Email Hook started'
                SMTPserver = transaction['request']['headers']['Testing-domain']
                testbox = testboxemail + SMTPserver

                USERNAME = testbox
                
                # Test of server SMTP recieveing emails from Dredd	
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
                time.sleep(wait_before_pop3)

                # Check POP3 message is in box
                
                box = poplib.POP3(SMTPserver)
                box.user(USERNAME)
                box.pass_(PASSWORD)

                #Get messages from server:
                messages = [box.retr(i) for i in range(1, len(box.list()[1]) + 1)]
                # Concat message pieces:
                messages = ["\n".join(mssg[1]) for mssg in messages]
                #Parse message intom an email object:
                messages = [parser.Parser().parsestr(mssg) for mssg in messages]
                
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
                # Set to success
                transaction['real']['statusCode'] = 299
                transaction['real']['body'] = ''
