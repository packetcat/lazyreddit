#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
#import smtplib
import configparser
#import datetime
#import pprint
import os
#from email.mime.text import MIMEText

# Variables
subreddits = []
submissions_final = []
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

def gethotposts(subreddits_list):
    # get subreddit object
    subreddit_data = r.get_subreddit(subreddits_list)
    # get hot posts generator object
    hot_posts = subreddit_data.get_hot()
    # lets get the output finally
    for submissions in hot_posts:
        text = str(submissions)
        print(text)

for subreddits in subreddits:
    gethotposts(subreddits)

# E-mail functionality
#now = datetime.datetime.now().strftime("%d-%m-%Y")   # the current date for e-mail's subject
# The actual message to be sent
#message = MIMEText(pprint.pformat(submissions_final, 6))
#message['Subject'] = "Your top subreddit submissions on %s" % now
#message['From'] = fromemail
#message['To'] = destemail
#print(message)
# Sending the message
#smtpObj = smtplib.SMTP(smtpserver, smtpport)
#smtpObj.starttls()
#smtpObj.login(smtpusername, smtppassword)
#smtpObj.sendmail(message['From'], message['To'], message.as_string())
#smtpObj.quit()
