#! /usr/local/bin/python
"""Sends an actionable message with the mail.html payload
Usage: 'send.py -u <username> -p <password> [-r <recipient>] [-f <paylod file name>]'
"""

import sys
import getopt
from smtplib import SMTP as SMTP
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

def main(argv):
    """The entry point for the script"""
    sender = ""
    password = ""
    recipient = ""
    payload_file = ""

    try:
        opts, _args = getopt.getopt(argv, 'u:p:r:f:', ['user=', 'password=', 'recipient=', 'file='])
    except getopt.GetoptError:
        print('send.py -u <username> -p <password> [-r <recipient>]  [-f <paylod file name>]')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u':
            sender = arg
        elif opt == '-p':
            password = arg
        elif opt == '-r':
            recipient = arg
        elif opt == '-f':
            payload_file = arg

    if (not sender) or (not password):
        print('send.py -u <username> -p <password> [-r <recipient>]  [-f <paylod file name>]')
        sys.exit(2)

    print('Sending mail from', sender)
    send_message(sender, password, recipient, payload_file)

def send_message(sender, password, recipient, payload_file):
    """Sends a message from sender to self
    Keyword arguments:
    sender -- The email address of the user that will send the message
    password -- The password for the user
    recipient -- (Optional)The recipient email address. Default to sender
    """

    if (not recipient):
        recipient = sender

    if (not payload_file):
        payload_file = "mail.html"
        
    html_content = ""
    with open(payload_file, 'r') as myfile:
        html_content = myfile.read()

    msg = MIMEText(html_content, 'html')
    msg['Subject'] = 'Test message'
    msg['From'] = sender

    conn = SMTP(SMTP_SERVER, SMTP_PORT)
    try:
        conn.starttls()
        conn.set_debuglevel(False)
        conn.login(sender, password)
        conn.sendmail(sender, recipient, msg.as_string())
    finally:
        conn.quit()

    print('Sent the mail')

if __name__ == '__main__':
    main(sys.argv[1:])