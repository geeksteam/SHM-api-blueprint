import smtplib
import poplib, email

import sys
import os
import re

from email.mime.text import MIMEText

# from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

import time
import dredd_hooks as hooks

# Global settings
SMTPserver = 'test.com'
testbox =     'info@test.com'
destination = ['kalashnikovm@mail.ru']

USERNAME = testbox
PASSWORD = "infoPassword"

text_subtype = 'plain'
content="""\
Dredd SMTP AUTH sending test message
"""
subject="Sent from Dredd SMTP AUTH test"


@hooks.before('Email boxes > List Email boxes > List email boxes')
def test_email(transaction):
        if transaction['skip'] != True:		
        
                # Test of server SMTP recieveing emails from Dredd	
                dreddsender = 'dredd-test@geeks.team'
                receivers = ['info@test.com']

                message = """From: Dredd <dredd-test@lgeeks.team>
                To: Test Server <info@test.com>
                Subject: SMTP e-mail Dredd test

                This is a test e-mail message.
                """
                try:
                        smtpObj = smtplib.SMTP('localhost')
                        smtpObj.sendmail(dreddsender, receivers, message)         
                        print "Successfully sent email"
                except:
                        transaction["fail"] = "Error: unable to send email by Dredd smtp"
                        
                # Send email using SMTP AUTH
                try:
                        msg = MIMEText(content, text_subtype)
                        msg['Subject']= subject
                        msg['From']   = testbox # some SMTP servers will do this automatically, not all

                        conn = SMTP(SMTPserver)
                        conn.set_debuglevel(False)
                        conn.login(USERNAME, PASSWORD)
                        conn.sendmail(testbox, destination, msg.as_string())
                        conn.quit()

                except Exception, exc:
                        transaction["fail"] = "SMTP AUTH mail failed; %s" % str(exc)
                        
                # Check POP3 message is in box
                
                box = poplib.POP3(SMTPserver)
                try:
                        box.user(USERNAME)
                        box.pass_(PASSWORD)
                except:
                        transaction["fail"] = "Dredd SMTP AUTH failed."
                
                response, lst, octets = box.list()
                print "DEBUG: Total %s messages: %s" % (login, len(lst))
                total_messages = len(lst)
                
                message_found = False
                for msgnum, msgsize in [i.split() for i in lst]:
                        (resp, lines, octets) = box.retr(msgnum)
                        msgtext = "n".join(lines) + "nn"
                        message = email.message_from_string(msgtext) 
                        # Check for message from Dredd
                        if message["subject"] == "SMTP e-mail Dredd test":
                                message_found = True
                                
                        print(msgtext)
                        box.dele(msgnum)
                
                box.quit()
                
                if message_found == False:
                        transaction["fail"] = "Dredd POP3 client failed: Message from DREDD not found in messages list. Total messages: %s" % total_messages
                        