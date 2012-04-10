#!/usr/bin/env python
# -*- coding: utf-8 -*-

import reddit, ConfigParser, email
from subprocess import call

# Read config file

config = ConfigParser.ConfigParser()
config.read('lazyreddit.cfg')

email = config.get('main', 'email')
subreddits = config.get('main', 'subreddits')

# Set user agent as needed
r = reddit.Reddit(user_agent="lazyreddit")
# parse subreddits further

subreddits = [y.strip().lower() for y in subreddits.split(',')]
u = unicode('s', "utf-8")
submissions = {}
for index in range(len(subreddits)):
    submissions[subreddits[index]] = [str(x) for x in r.get_subreddit(subreddits[index]).get_top(limit=10)]

# Code below is for debugging purposes
for k, v in submissions.iteritems():
	print k,v

for index in range(len(subreddits)):
	print 'Subreddit', subreddits[index]