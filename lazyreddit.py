#!/usr/bin/env python
# -*- coding: utf-8 -*-

import narwal, ConfigParser, smtplib, socket, datetime
from subprocess import call

# Read config file

config = ConfigParser.ConfigParser()
config.read('lazyreddit.cfg')

email = config.get('main', 'email')
subreddits = config.get('main', 'subreddits')

# Set user agent as needed
r = narwal.connect(user_agent="lazyreddit")
# parse subreddits further

subreddits = [y.strip().lower() for y in subreddits.split(',')]
submissions = {}
for index in range(len(subreddits)):
    submissions[subreddits[index]] = [str(x) for x in r.hot(sr=subreddits[index], limit=10)]

# E-mail functionality
for k, v in submissions.iteritems():
	print k,v

hostname = socket.gethostname()
sender = "lazyreddit@" + hostname
now = datetime.datetime.now() # Gets the current date for e-mail's subject
currentdate = now.strftime("%d-%m-%Y") # formats the date properly
# The actual message to be sent
message = """From: Lazyreddit <""" + sender + """>
To: A Redditor <""" + email + """>
Subject: Your top subreddit submssions on """ + currentdate + """

""" + str(submissions['linux'])

# Sending the message
try:
    smtpObj = smtplib.SMTP('localhost') # assuming you have a local SMTP server
    smtpObj.sendmail(sender, email, message)
    print "Successfully sent e-mail!"
except SMTPException:
    print "Error: unable to send e-mail!"
