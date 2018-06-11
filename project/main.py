#!/usr/bin/env python3

import argparse
import json
from handlers import Handler
from sys import stdin

parser = argparse.ArgumentParser(description="Access the X company's database")
parser.add_argument('--init', action='store_true')

args = parser.parse_args()

def init_mode():
    handler = Handler('init')
    for line in stdin:
        try:
            res = handler.handle(line)
        except Exception as e:
            msg = '{}: {}'.format(type(e), e)
            res = {'status': 'ERROR', 'debug': msg}
        print(json.dumps(res))
    
def app_mode():
    handler = Handler()
    for line in stdin:
        try:
            res = handler.handle(line)
        except Exception as e:
            msg = '{}: {}'.format(type(e), e)
            res = {'status': 'ERROR', 'debug': msg}
        print(json.dumps(res))

if args.init:
    init_mode()
else:
    app_mode()
