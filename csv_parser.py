#!/usr/bin/env python

import argparse
import csv


def parse_input():
    "Parse user input"

    parser = argparse.ArgumentParser(description='CSV Parser')

    parser.add_argument('--file', required=True, help='File to parse')

    parser.add_argument('--column', required=True, type=int, help='The column number indexed from 0')

    parser.add_argument('--delimiter', choices=['tab', 'comma', 'pipe'], default='tab')

    args = parser.parse_args()

    return args


def set_delimiter(delimiter):
  if delimiter == 'tab':
    return '\t'
  elif delimiter == 'comma':
    return ','
  elif delimiter == 'pipe':
    return '|'
  else:
    return None


def main():
  args = parse_input()

  handles = {}
  delimiter = set_delimiter(args.delimiter)

  with open(args.file, 'rb') as csvfile:
    r = csv.reader(csvfile, delimiter=delimiter)
    for row in r:
      key = '{0}'.format(row[args.column])
      if key in handles.keys():
        handles[key] += 1
      else:
        handles[key] = 1

  for key in handles.keys():
    print('{0}\t{1}'.format(key, handles[key]))


if __name__ == '__main__':
  main()
