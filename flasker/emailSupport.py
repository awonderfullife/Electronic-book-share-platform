# -*- coding:utf-8

import smtplib
from email.mime.text import MIMEText

import config


def send_mail(me, you, subject, content):
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    # textfile = 'mail.txt'
    # fp = open(textfile, 'rb')
    # Create a text/plain message
    msg = MIMEText(content)
    # fp.close()

    # me == the sender's email address
    # you == the recipient's email address

    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    # s = smtplib.SMTP('localhost')
    server = smtplib.SMTP('smtp.163.com', 25)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
    re = server.sendmail(me, [you], msg.as_string())
    print re
    server.quit()
