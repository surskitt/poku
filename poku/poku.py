# -*- coding: utf-8 -*-

"""Main module."""

import sys
import configargparse
import requests


def parse_args(args):
    """ parse arguments using configargparse module """
    conf_files = ['/etc/poku/*.cfg', '~/.config/poku/*.cfg']
    parser = configargparse.ArgParser(default_config_files=conf_files)
    parser.add('--consumer', required=True)
    parser.add('--access')
    args = parser.parse_args(args)

    return args


def get_pocket_response_token(consumer):
    """ get response token from api """
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


def generate_pocket_auth_url(request_token):
    """ return auth url for user to authorize application """
    url = ('https://getpocket.com/auth/authorize'
           '?request_token={0}'
           '&redirect_uri=https://getpocket.com').format(request_token)

    return url


def get_pocket_access_token(consumer_key, request_token):
    """ get access token from api """
    data = {
        'consumer_key': consumer_key,
        'code': request_token
    }
    r = requests.get('https://getpocket.com/v3/oauth/authorize', data=data)
    if r.ok:
        return r.json()['access_token']
    else:
        return None


def get_pocket_items(consumer_key, access_token):
    """ get a list pocket items from api """
    data = {
        'consumer_key': consumer_key,
        'access_token': access_token
    }
    r = requests.get('https://getpocket.com/v3/get', data=data)

    if r.ok:
        return [i for i in r.json()['list'].values()]
    else:
        return None


def sort_pocket_items(item_list):
    """ sort list of pocket items based on update time """
    return sorted(item_list, key=lambda x: x['time_updated'])
