#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for main calling function. """

from unittest.mock import patch

import poku


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
    mock_parse_args.return_value.tag = None
    mock_poku_diff.return_value = [{'url': 'a', 'title': 'b', 'tags': ['c']}]

    poku.poku.main()

    mock_buku.return_value.add_rec.assert_called_once()


@patch('poku.poku.parse_args')
@patch('poku.pocket')
@patch('poku.poku.buku.BukuDb')
@patch('poku.buku.tags_to_tagstring')
@patch('poku.utils.dict_list_difference')
def test_tag_is_added_for_imported_items(mock_poku_diff,
                                         mock_tags_to_tagstring, mock_buku,
                                         mock_pocket, mock_parse_args):
    mock_parse_args.return_value.tag = 'foo'
    mock_poku_diff.return_value = [{'url': 'a', 'title': 'b', 'tags': ['c']}]

    poku.poku.main()

    mock_tags_to_tagstring.assert_called_once_with(['c', 'foo'])
