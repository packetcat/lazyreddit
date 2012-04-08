#!/usr/bin/env python

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

#for subreddits in subreddits:
#	topten = r.get_subreddit(subreddits[0]).get_top(limit=10)

i = 0
topten = []
for i in len(subreddits):
	topten[i] = r.get_subreddit(subreddits[i].get_top(limit=10))
	i += 1

print topten[0]