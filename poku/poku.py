# -*- coding: utf-8 -*-

"""Main module."""

import configargparse
import requests


def parse_args(args):
    """ Parse arguments using configargparse module """
    conf_files = ['/etc/poku/*.cfg', '~/.config/poku/*.cfg']
    parser = configargparse.ArgParser(default_config_files=conf_files)
    parser.add('--consumer', '-p', required=True)

    return parser.parse_args(args)


def get_response_token(consumer):
    data = {
        'consumer_key': consumer,
        'redirect_uri': 'https://getpocket.com'
    }
    r = requests.get('https://getpocket.com/v3/oauth/request', data=data)
    if r.ok:
        return r.text.split('=')[1]
    else:
        return None


def generate_auth_url(token):
    url = ('https://getpocket.com/auth/authorize'
           '?request_token={0}'
           '&redirect_uri=https://getpocket.com').format(token)

    return url
