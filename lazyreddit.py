#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import smtplib
import configparser
import datetime
import pprint
import os
from email.mime.text import MIMEText

# Variables
subreddits = []
submissions = {}

# Set user agent as needed
r = praw.Reddit(user_agent='lazyreddit-nextgen')
configfilepath = os.path.join(os.getcwd(), "lazyreddit.cfg")
config = configparser.ConfigParser()

if os.path.isfile(configfilepath) is False:
    print ("A config file does not exist, see source for an example.")
    raise SystemExit
else:
    config.read(configfilepath)
    destemail = config.get('main', 'destemail')
    subreddits = config.get('main', 'subreddits')
    smtpserver = config.get('smtp', 'smtpserver')
    smtpusername = config.get('smtp', 'username')
    smtppassword = config.get('smtp', 'password')
    smtpport = config.get('smtp', 'portnumber')
    fromemail = config.get('smtp', 'fromemail')
    subreddits = [y.strip().lower() for y in subreddits.split(',')]

# parse subreddits further
for subreddits in subreddits:
    submissions[subreddits] = ([str(x) for x in
                                r.hot(sr=subreddits, limit=10)])

# E-mail functionality
now = datetime.datetime.now().strftime("%d-%m-%Y")   # the current date for e-mail's subject
# The actual message to be sent
message = MIMEText(pprint.pformat(submissions, 6))
message['Subject'] = "Your top subreddit submissions on %s" % now
message['From'] = fromemail
message['To'] = destemail

# Sending the message
smtpObj = smtplib.SMTP(smtpserver, smtpport)
smtpObj.starttls()
smtpObj.login(smtpusername, smtppassword)
smtpObj.sendmail(message['From'], message['To'], message.as_string())
print ("Successfully sent e-mail!")
smtpObj.quit()
