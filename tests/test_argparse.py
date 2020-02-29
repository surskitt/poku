#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for argument parsing. """

from unittest.mock import patch, mock_open
import pytest

import poku


@pytest.fixture
def mandatory_args():
    return [
        '--consumer', 'abc'
    ]


def test_parse_consumer(mandatory_args):
    """ Test that a consumer argument is handled and received """
    args = poku.poku.parse_args(mandatory_args + ['--consumer', 'def'])
    assert args.consumer == 'def'


def test_parse_access_token(mandatory_args):
    """ Test that an access token argument is handled and received """
    args = poku.poku.parse_args(mandatory_args + ['--access', 'ghi'])
    assert args.access == 'ghi'


@patch('builtins.open', mock_open(read_data=""))
def test_no_consumer():
    """ Test that missing out the consumer argument causes a system exit """
    with pytest.raises(SystemExit):
        poku.poku.parse_args([])


@patch('poku.pocket.requests.post')
def test_get_access_token_not_ok(mock_get):
    """ test that unsuccessful access token requests return None """
    mock_get.return_value.ok = False

    exception_msg = 'An error occured while requesting access token'
    with pytest.raises(poku.exceptions.PocketGetAccessTokenException,
                       match=exception_msg):
        poku.pocket.get_access_token('ck', 'rt')


@patch('poku.pocket.requests.post')
def test_get_pocket_items(mock_get):
    """ test that pocket items requests returns expected list """
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {'list': {'a': 't1', 'b': 't2'}}
    expected = ['t1', 't2']

    pocket_items = sorted(poku.pocket.get_items('ck', 'at'))
    assert pocket_items == expected


@patch('poku.pocket.requests.post')
def test_get_pocket_items_not_ok(mock_get):
    """ test that unsuccessful pocket items requests return None """
    mock_get.return_value.ok = False

    exception_msg = 'An error occured while retrieving pocket items'
    with pytest.raises(poku.exceptions.PocketGetItemsException,
                       match=exception_msg):
        poku.pocket.get_items('ck', 'at')


def test_pocket_item_to_dict():
    """ test converting of pocket item to universal item """
    pocket_item = {
        'resolved_url': 'test.com',
        'resolved_title': 'test page',
        'tags': {'test': {}, 'test2': {}},
        'time_added': '1'
    }
    expected = {
        'url': 'test.com',
        'title': 'test page',
        'tags': ['test', 'test2'],
        'timestamp': 1
    }

    dict_item = poku.pocket.item_to_dict(pocket_item)
    assert dict_item == expected
