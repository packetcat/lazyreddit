#!/usr/bin/env python

import reddit, ConfigParser, email
from subprocess import call

# Read config file

config = ConfigParser.ConfigParser()
config.read('lazyreddit.cfg')

email = config.get('main', 'email')
subreddits = config.get('main', 'subreddits')

# parse subreddits further

subreddits = [y.strip().lower() for y in subreddits.split(',')]

print subreddits