#!/usr/bin/env python
# -*- coding: utf-8 -*-

import narwal
import smtplib
import ConfigParser
import socket
import datetime
import pprint
import os

# Variables
subreddits = []
submissions = {}

# Set user agent as needed
r = narwal.connect(user_agent="lazyreddit")
configfilepath = os.path.join(os.getcwd(), "lazyreddit.cfg")
config = ConfigParser.ConfigParser()

if os.path.isfile(configfilepath) == False:
    print "A config file does not exist, get one from here - http://goo.gl/znYqb"
    raise SystemExit
else:
    config.read(configfilepath)
    email = config.get('main', 'email')
    subreddits = config.get('main', 'subreddits')
    smtpserver = config.get('main', 'smtpserver')
    subreddits = [y.strip().lower() for y in subreddits.split(',')]

# parse subreddits further
for subreddits in subreddits:
    submissions[subreddits] = ([str(x) for x in
                                      r.hot(sr=subreddits, limit=10)])

# E-mail functionality
hostname = socket.gethostname()
sender = "lazyreddit@" + hostname
now = datetime.datetime.now()   # the current date for e-mail's subject
currentdate = now.strftime("%d-%m-%Y")   # formats the date properly
# The actual message to be sent
message = """From: Lazyreddit <""" + sender + """>
To: A Redditor <""" + email + """>
Subject: Your top subreddit submissions on """ + currentdate + """

""" + pprint.pformat(submissions, 6)

# Sending the message
try:
    smtpObj = smtplib.SMTP(smtpserver)
    smtpObj.sendmail(sender, email, message)
    print "Successfully sent e-mail!"
except smtplib.SMTPException:
    print "Error: unable to send e-mail!"
