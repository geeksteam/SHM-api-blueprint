import smtplib
import poplib, email

import sys
import os
import re
import time
import json

from email.mime.text import MIMEText

import time
import dredd_hooks as hooks

# Global settings
testboxemail =     'info@'
destination = ['kalashnikovm@mail.ru']

# USERNAME = testboxemail@server
PASSWORD = "infoPassword"

# Wait until pop3 test
wait_before_pop3 = 15


@hooks.before_validation('Email boxes > @Hook pop3/smtp testing > @Hook pop3/smtp testing')
def test_email(transaction):
        if transaction['skip'] != True:

                SMTPserver = transaction['request']['headers']['Testing-domain']
                testbox = testboxemail + SMTPserver

                USERNAME = testbox
        
                transaction['real']['body'] = "Dredd testing"
                
                # Test of server SMTP recieveing emails from Dredd	
                dreddsender = 'dredd-test@geeks.team'
                receivers = [testbox]

                message = """From: Dredd <dredd-test@geeks.team>
                To: <%s>
                Subject: SMTP e-mail Dredd RECIEVE test

                This is a test e-mail message.
                """ % testbox

                smtpObj = smtplib.SMTP('localhost')
                smtpObj.set_debuglevel(True)
                smtpObj.sendmail(dreddsender, receivers, message)         
                print "Successfully sent email"
                smtpObj.quit()
                        
                # Send email using SMTP AUTH
                message = """From: Dredd <%s>
                To: <max@geeks.team>
                Subject: SMTP e-mail Dredd AUTH test

                This is a test e-mail message.
                """ % testbox
                conn = smtplib.SMTP(SMTPserver)
                conn.set_debuglevel(True)
                
                conn.login(USERNAME, PASSWORD)
                conn.sendmail(testbox, destination, message)
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
                        print >> sys.stderr, 'Got Message: %s' % message['from']
                        # Check for message from Dredd
                        if "<dredd-test@geeks.team>" in message['from'] :
                                message_found = True
                        # Delete message
                        box.dele(i)
                box.quit()
                
                if message_found == False:
                        transaction["fail"] = "Dredd POP3 client failed: Message from DREDD not found in messages list. Total messages: %s" % total_messages
                # Set to success
                transaction['real']['statusCode'] = 202
                transaction['real']['body'] = ''
