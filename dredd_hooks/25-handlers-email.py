import smtplib
import time
import dredd_hooks as hooks

# Test of server SMTP recieveing email
@hooks.after('Email boxes > List Email boxes > List email boxes')
def test_email_smtp_recieve(transaction):
        if transaction['skip'] != True:				
                sender = 'dredd-test@lgeeks.team'
                receivers = ['info@test.com']

                message = """From: Dredd <dredd-test@lgeeks.team>
                To: Test Server <info@test.com>
                Subject: SMTP e-mail test

                This is a test e-mail message.
                """
                try:
                        smtpObj = smtplib.SMTP('localhost')
                        smtpObj.sendmail(sender, receivers, message)         
                        print "Successfully sent email"
                except SMTPException:
                        transaction["fail"] = "Error: unable to send email by Dredd smtp"
