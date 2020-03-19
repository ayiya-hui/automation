#!/usr/bin/python

#phsendsecuremail.py to send mail with auth

import os,sys
import smtplib
#from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
  if ( len(sys.argv) < 9 ):
    print('Usage: %s mailhost port user pswd from recipient subject message' % sys.argv[0])
    sys.exit(1)

  host = sys.argv[1]
  port = sys.argv[2]
  user = sys.argv[3]
  pswd = sys.argv[4]
  sender = sys.argv[5]
  recipient = sys.argv[6]
  subject = sys.argv[7]
  message = sys.argv[8]

  server = smtplib.SMTP(host, port);
  #server.set_debuglevel(1)
  server.ehlo()
  server.starttls()
  server.ehlo()
  server.login(user, pswd)

  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject ;
  msg['From'] = sender ;
  msg['To'] = recipient

  html = MIMEText(message, 'html')
  msg.attach(html)
  toaddrs = recipient.split()
  server.sendmail(sender, toaddrs, msg.as_string())

  server.quit()
  sys.exit( 0 );

main ()

