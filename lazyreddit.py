#!/usr/bin/env python
# -*- coding: utf-8 -*-

import narwal
import ConfigParser
import smtplib
import socket
import datetime
import pprint
import sys
import argparse
import os

# Variables
subreddits = []
# Argument stuff
parser = argparse.ArgumentParser(description='lazyreddit - A program that e-mails you top posts from chosen subreddits.')
parser.add_argument('--version', action='version', version='lazyreddit v0.1')
parser.add_argument('--noconfigfile', action='store', default="False", help='Use commandline arguments instead of a config file, set as "False" by default')
parser.add_argument('-e', action='store', help='Specify the e-mail to send the submissions to.', type=str)
parser.add_argument('-subs', action='append', help='Specify the subreddits to get submissions from, use multiple times to specify multiple subreddits.')
parser.add_argument('-smtpserver', action='store', help='Specify the SMTP server to use to send the e-mail.')
args = vars(parser.parse_args())

configfilepath = os.path.join(os.getcwd(), "lazyreddit.cfg")
config = ConfigParser.ConfigParser()
cli_options = args['noconfigfile']

if cli_options == "True":
    print "using CLI args instead of config file"
    email = args['e']
    subreddits = args['subs']
    smtpserver = args['smtpserver']
else:
    if os.path.isfile(configfilepath) == False:
        print "A config file does not exist, get one from here - http://goo.gl/znYqb"
        raise SystemExit
    else:
        config.read('lazyreddit.cfg')
    email = config.get('main', 'email')
    subreddits = config.get('main', 'subreddits')
    smtpserver = config.get('main', 'smtpserver')
    subreddits = [y.strip().lower() for y in subreddits.split(',')]

# Set user agent as needed
r = narwal.connect(user_agent="lazyreddit")

# parse subreddits further
submissions = {}
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
Subject: Your top subreddit submssions on """ + currentdate + """

""" + pprint.pformat(submissions, 6)

# Sending the message
try:
    smtpObj = smtplib.SMTP(smtpserver)
    smtpObj.sendmail(sender, email, message)
    print "Successfully sent e-mail!"
except smtplib.SMTPException:
    print "Error: unable to send e-mail!"
