# -*- coding: utf-8 -*-

""" Pocket specific utils """

import logging
import requests

import poku.exceptions


def get_request_token(consumer_key):
    """ get request token from api """
    data = {'consumer_key': consumer_key, 'redirect_uri': 'getpocket.com'}
    headers = {'x-accept': 'application/json'}
    r = requests.post('https://getpocket.com/v3/oauth/request',
                      data=data, headers=headers)

    if r.ok:
        request_token = r.json()['code']
        logging.info(f'Request token retrived successfully: {request_token}')
        return request_token
    else:
        exception_msg = 'An error occured while requesting request token'
        raise poku.exceptions.PocketGetRequestTokenException(exception_msg)


def generate_auth_url(request_token):
    """ return auth url for user to authorize application """
    url = ('https://getpocket.com/auth/authorize'
           f'?request_token={request_token}'
           '&redirect_uri=https://getpocket.com')

    return url


def get_access_token(consumer_key, request_token):
    """ get access token from api """
    data = {'consumer_key': consumer_key, 'code': request_token}
    headers = {'x-accept': 'application/json'}
    r = requests.post('https://getpocket.com/v3/oauth/authorize',
                      data=data, headers=headers)

    if r.ok:
        access_token = r.json()['access_token']
        logging.info(f'Access token retrieved successfully: {access_token}')
        return access_token
    else:
        exception_msg = 'An error occured while requesting access token'
        raise poku.exceptions.PocketGetAccessTokenException(exception_msg)


def get_items(consumer_key, access_token):
    """ get a list pocket items from api """
    data = {
        'consumer_key': consumer_key,
        'access_token': access_token,
        'detailType': 'complete'
    }
    r = requests.post('https://getpocket.com/v3/get', data=data)

    if r.ok:
        pocket_items = [i for i in r.json()['list'].values()]
        logging.info(f'{len(pocket_items)} pocket items retrieved')
        return pocket_items
    else:
        exception_msg = 'An error occured while retrieving pocket items'
        raise poku.exceptions.PocketGetItemsException(exception_msg)


def item_to_dict(p_item):
    """ convert pocket item to universal dict """
    out = {
        'url': p_item.get('resolved_url') or p_item.get('given_url'),
        'title': p_item.get('resolved_title') or p_item.get('given_title'),
        'tags': sorted(p_item.get('tags', {}).keys()),
        'timestamp': int(p_item.get('time_updated'))
    }

    return out
