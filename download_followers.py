#!/usr/bin/env python

import argparse

import tweepy


def main():
  creds = {}

  creds['consumer_key'] = raw_input('Consumer Key: ')
  creds['consumer_secret'] = raw_input('Consumer Secret: ')
  creds['access_token'] = raw_input('Access Token: ')
  creds['access_token_secret'] = raw_input('Access Token Secret: ')
  output_filename = raw_input('Output filename: ')
  screen_name = raw_input('Screen name: ')

  auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
  auth.set_access_token(creds['access_token'], creds['access_token_secret'])

  api = tweepy.API(auth, wait_on_rate_limit=True)

  ids = []

  for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
    ids.extend(page)

  print("Total followers: {0}".format(len(ids)))

  print("OK, looking up user screen names now")

  chunk_size = 100
  users_chunked = [ids[i:i + chunk_size] for i in xrange(0, len(ids), chunk_size)]

  with open(output_filename, 'w') as f:
    for user_ids in users_chunked:
      users = api.lookup_users(user_ids=user_ids)
      for u in users:
        f.write("{0}\t{1}\n".format(u.id, u.screen_name))

if __name__ == '__main__':
  main()
