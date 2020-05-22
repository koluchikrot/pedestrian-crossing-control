"""
This file is responsible for sending e-mails
"""

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from _datetime import datetime

email = 'icrosssystem@mail.ru'
password = 'keklol12345'


def send(send_to, name, img_send):
    """
    this function sends email from email
    to send_to address
    with message in notification
    """
    msg = MIMEMultipart()

    s = name + ",\nВы нарушили ПДД " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    part = MIMEText(s, 'plain', 'utf-8')
    msg.attach(part)
    part = MIMEApplication(open(img_send, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=img_send)
    msg.attach(part)
    msg['Subject'] = Header('Нарушение', 'utf-8')
    msg['From'] = email
    msg['To'] = send_to
    # Connecting to the mail server
    # The first argument is a domain name, the second is the port number
    smtpo = smtplib.SMTP('smtp.mail.ru', 587)

    # Using protocol TLS
    ready = smtpo.starttls()
    # Confirmation
    out = (220, b'2.0.0 Start TLS')
    if ready == out:
        # Authorization
        smtpo.login(email, password)
        # Send a mail to send_to with  text notification
        smtpo.sendmail(email, send_to, msg.as_string())
