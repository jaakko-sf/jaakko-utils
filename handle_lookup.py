#!/usr/bin/env python

import argparse
from os.path import expanduser

import tweepy
import yaml


def parse_input():
  "Parse user input"

  parser = argparse.ArgumentParser(description='Twitter Handle Lookup')

  parser.add_argument('--file', required=True, help='File to parse handles from')

  args = parser.parse_args()

  return args


def load_twurlrc():
  """Load the default profiles creds"""

  path = expanduser("~")

  with open(path + '/.twurlrc', 'r') as stream:
    data = yaml.load(stream)

  handle, consumer_key = data['configuration']['default_profile']

  creds = {
    'consumer_key': consumer_key,
    'consumer_secret': data['profiles'][handle][consumer_key]['consumer_secret'],
    'access_token': data['profiles'][handle][consumer_key]['token'],
    'access_token_secret': data['profiles'][handle][consumer_key]['secret']
  }

  return creds


def main():
  args = parse_input()

  # load creds from .twurlrc
  creds = load_twurlrc()

  # get data from twitter api
  auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
  auth.set_access_token(creds['access_token'], creds['access_token_secret'])

  api = tweepy.API(auth, wait_on_rate_limit=True)

  with open(args.file, 'r') as data:
    for row in data:
      handle_name = row.rstrip()

      try:
        user = api.get_user(handle_name)
        user_id = user.id
      except:
        user_id = 'does not exist'

      print('{1}\t{0}'.format(handle_name, user_id))


if __name__ == '__main__':
  main()
