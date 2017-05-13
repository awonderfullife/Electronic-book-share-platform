# -*- coding:utf-8

import smtplib
from email.mime.text import MIMEText

import config


def send_mail(me, you, subject, content):
    msg = MIMEText(content)

    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    server = smtplib.SMTP('smtp.163.com', 25)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
    re = server.sendmail(me, [you], msg.as_string())
    print re
    server.quit()
