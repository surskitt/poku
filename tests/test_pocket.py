#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for pocket functions. """

from unittest.mock import patch
import pytest

import poku


@patch('poku.pocket.requests.post')
def test_get_request_token(mock_get):
    """ Test if successful token requests return expected token """
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {'code': 'b'}

    token = poku.pocket.get_request_token('abc')
    assert token == 'b'


@patch('poku.pocket.requests.post')
def test_get_request_token_not_ok(mock_get):
    """ Test that unsuccessful token requests return exception """
    mock_get.return_value.ok = False

    exception_msg = 'An error occured while requesting request token'
    with pytest.raises(poku.exceptions.PocketGetRequestTokenException,
                       match=exception_msg):
        poku.pocket.get_request_token('abc')


def test_generate_auth_url():
    """ test that expected auth url is generated """
    token = 'hello'
    expected_url = ('https://getpocket.com/auth/authorize'
                    '?request_token={0}'
                    '&redirect_uri=https://getpocket.com').format(token)

    url = poku.pocket.generate_auth_url(token)
    assert url == expected_url


@patch('poku.pocket.requests.post')
def test_get_access_token(mock_get):
    """ test access token requests """
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {'access_token': 'a'}

    atoken = poku.pocket.get_access_token('ck', 'rt')
    assert atoken == 'a'
