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
PASSWORD = "testpass"


@hooks.after('Email boxes > List Email boxes > List email boxes')
def test_email(transaction):
        if transaction['skip'] != True:		
        
                transaction['real']['body'] = "Dredd testing"
                
                # Test of server SMTP recieveing emails from Dredd	
                dreddsender = 'dredd-test@geeks.team'
                receivers = [testbox]

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
                        return
                        
                # Send email using SMTP AUTH
                try:
                        
                        message = """From: Dredd <info@test.com>
To: <max@geeks.team>
Subject: SMTP e-mail Dredd AUTH test

This is a test e-mail message.
"""

                        conn = smtplib.SMTP(SMTPserver)
                        conn.set_debuglevel(True)
                        
                        conn.login(USERNAME, PASSWORD)
                        conn.sendmail(testbox, destination, message)
                        
                        conn.quit()

                except Exception, exc:
                        transaction["fail"] = "SMTP AUTH mail failed; %s" % str(exc)
                        return
                        
                # Check POP3 message is in box
                
                box = poplib.POP3(SMTPserver)
                try:
                        box.user(USERNAME)
                        box.pass_(PASSWORD)
                
                        response, lst, octets = box.list()
                        print "DEBUG: Total messages: %s" % len(lst)
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
                        
                except:
                        transaction["fail"] = "Dredd POP3 Client LOGIN or MESSAGE LIST/DELETE failed."
                        return
                
                if message_found == False:
                        transaction["fail"] = "Dredd POP3 client failed: Message from DREDD not found in messages list. Total messages: %s" % total_messages
                        