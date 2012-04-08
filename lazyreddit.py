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

i = 0
for i in range(len(subreddits)):
    submissions = list(r.get_subreddit(subreddits[i]).get_top(limit=10))
    i += 1

print submissions[1]
