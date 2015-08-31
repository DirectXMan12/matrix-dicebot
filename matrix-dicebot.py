#!/usr/bin/env python
import argparse

from dicebot import bot
from dicebot.backends import matrix

parser = argparse.ArgumentParser(description='A Dicebot for Matrix')
parser.add_argument('--user', help='the username for dicebot to use',
                    default='dicebot')
parser.add_argument('--password', help='the password for dicebot to use')
parser.add_argument('--server', help='the Matrix server to which to connect',
                    default='https://matrix.org/')

args = parser.parse_args()

backend = matrix.MatrixBackend(bot.TextHandler, args.server, args.user, args.password)
backend.begin()
