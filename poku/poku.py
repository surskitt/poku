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


def generate_auth_url(request_token):
    url = ('https://getpocket.com/auth/authorize'
           '?request_token={0}'
           '&redirect_uri=https://getpocket.com').format(request_token)

    return url


def get_access_token(consumer_key, request_token):
    data = {
        'consumer_key': consumer_key,
        'code': request_token
    }
    r = requests.get('https://getpocket.com/v3/oauth/authorize', data=data)
    if r.ok:
        return r.json()['access_token']
    else:
        return None
