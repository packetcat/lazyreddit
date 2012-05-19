#!/usr/bin/env python
# -*- coding: utf-8 -*-

import narwal
import ConfigParser
import smtplib
import socket
import datetime
import pprint
import os

configfilepath = os.path.join(os.getcwd(), "lazyreddit.cfg")
config = ConfigParser.ConfigParser()

# Check to see if config file exists and then loads it
if os.path.isfile(configfilepath) == False:
    print "A config file does not exist, get one from here - http://goo.gl/znYqb"
else:
    config.read('lazyreddit.cfg')

# Set values from config file
email = config.get('main', 'email')
subreddits = config.get('main', 'subreddits')
smtpserver = config.get('main', 'smtpserver')

# Set user agent as needed
r = narwal.connect(user_agent="lazyreddit")

# parse subreddits further
subreddits = [y.strip().lower() for y in subreddits.split(',')]
submissions = {}
for index in range(len(subreddits)):
    submissions[subreddits[index]] = ([str(x) for x in
                                      r.hot(sr=subreddits[index], limit=10)])

# E-mail functionality
hostname = socket.gethostname()
sender = "lazyreddit@" + hostname
now = datetime.datetime.now()   # the current date for e-mail's subject
currentdate = now.strftime("%d-%m-%Y")   # formats the date properly
# The actual message to be sent
message = """From: Lazyreddit <""" + sender + """>
To: A Redditor <""" + email + """>
Subject: Your top subreddit submssions on """ + currentdate + """

""" + pprint.pformat(submissions, 6)

# Sending the message
try:
    smtpObj = smtplib.SMTP(smtpserver)
    smtpObj.sendmail(sender, email, message)
    print "Successfully sent e-mail!"
except SMTPException:
    print "Error: unable to send e-mail!"
