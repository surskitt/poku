# -*- coding: utf-8 -*-

"""Main module."""

import sys
import configargparse
import requests


def parse_args(args):
    """ Parse arguments using configargparse module """
    conf_files = ['/etc/poku/*.cfg', '~/.config/poku/*.cfg']
    parser = configargparse.ArgParser(default_config_files=conf_files)
    parser.add('--consumer', required=True)
    parser.add('--access')
    args = parser.parse_args(args)

    return args


def get_response_token(consumer):
    data = {
        'consumer_key': consumer,
        'redirect_uri': 'https://getpocket.com'
    }
    headers = {
        'x-accept': 'application/json'
    }
    r = requests.get('https://getpocket.com/v3/oauth/request',
                     data=data, headers=headers)
    if r.ok:
        return r.json()['code']
    else:
        return None


def generate_auth_url(rtoken):
    url = ('https://getpocket.com/auth/authorize'
           '?request_token={0}'
           '&redirect_uri=https://getpocket.com').format(rtoken)

    return url


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
