#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `poku` package. """

from unittest.mock import patch
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


def test_no_consumer():
    """ Test that missing out the consumer argument causes a system exit """
    with pytest.raises(SystemExit):
        poku.poku.parse_args([])


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
        'time_updated': '1'
    }
    expected = {
        'url': 'test.com',
        'title': 'test page',
        'tags': ['test', 'test2'],
        'timestamp': 1
    }

    dict_item = poku.pocket.item_to_dict(pocket_item)
    assert dict_item == expected


def test_buku_item_to_dict():
    """ test converting of buku item to universal item """
    buku_item = (1, 'test.com', 'test page', ',test,test2,')
    expected = {
        'url': 'test.com',
        'title': 'test page',
        'tags': ['test', 'test2'],
        'timestamp': 1
    }

    dict_item = poku.buku.item_to_dict(buku_item)
    assert dict_item == expected


@pytest.mark.parametrize('tag_list,expected', [
    (['t1', 't2'], ',t1,t2,'),
    (['t1'], ',t1,'),
    ([], ',')
])
def test_buku_tags_to_tagstring(tag_list, expected):
    """ test coversion of list of tags to command separated string """
    tagstring = poku.buku.tags_to_tagstring(tag_list)
    assert tagstring == expected


@pytest.mark.parametrize('item_list', [
    [{'timestamp': '1'}, {'timestamp': '2'}],
    [{'timestamp': '2'}, {'timestamp': '1'}]
])
def test_sort_dict_items(item_list):
    """ test that items are being sorted correctly """
    expected = [{'timestamp': '1'}, {'timestamp': '2'}]
    sorted_list = poku.utils.sort_dict_items(item_list)

    assert sorted_list == expected


def test_dict_list_difference():
    """ test return of items in list1 but not in list2 """
    l1 = [{'url': 'a'}, {'url': 'b'}, {'url': 'c'}]
    l2 = [{'url': 'b'}, {'url': 'c'}]
    expected = [{'url': 'a'}]

    filtered_list = poku.utils.dict_list_difference(l1, l2)
    assert filtered_list == expected


def test_dict_list_ensure_unique():
    """ test ensuring list of items all have a unique url """
    item_list = [{'url': 'a', 't': 1},
                 {'url': 'a', 't': 2},
                 {'url': 'b', 't': 3}]
    expected = [{'url': 'a', 't': 2}, {'url': 'b', 't': 3}]

    unique_list = poku.utils.dict_list_ensure_unique(item_list)
    assert unique_list == expected


@patch('poku.poku.parse_args')
@patch('poku.poku.webbrowser')
@patch('builtins.input')
@patch('poku.pocket')
@patch('poku.poku.buku.BukuDb')
def test_fetch_access_token_if_no_arg(mock_buku, mock_pocket, mock_input,
                                      mock_browser, mock_parse_args):
    """ test to make sure access token retrieval is run if not in args """
    mock_parse_args.return_value.access = None

    poku.poku.main()

    mock_pocket.get_access_token.assert_called_once()


@patch('poku.poku.parse_args')
@patch('poku.pocket')
@patch('poku.poku.buku.BukuDb')
def test_skip_fetch_access_token_if_arg(mock_buku, mock_pocket,
                                        mock_parse_args):
    """ test to make sure access token retrieval is skipped if arg exists """
    mock_parse_args.return_value.access = 'token'

    poku.poku.main()

    mock_pocket.get_access_token.assert_not_called()


@patch('poku.poku.parse_args')
@patch('poku.pocket')
@patch('poku.poku.buku.BukuDb')
@patch('poku.utils.dict_list_difference')
def test_buku_add_is_run_when_new_items(mock_poku_diff, mock_buku, mock_pocket,
                                        mock_parse_args):
    mock_poku_diff.return_value = [{'url': 'a', 'title': 'b', 'tags': 'c'}]

    poku.poku.main()

    mock_buku.return_value.add_rec.assert_called_once()
