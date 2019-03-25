#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `poku` package."""

from unittest.mock import Mock, patch
import pytest


from poku import poku
import requests
import configargparse


def test_parse_consumer():
    """ Test that a consumer argument is handled and received """
    args = poku.parse_args(['--consumer', 'abc'])
    assert args.consumer == 'abc'


def test_no_consumer():
    """ Test that missing out the consumer argument causes a system exit """
    with pytest.raises(SystemExit):
        args = poku.parse_args([])


@patch('poku.poku.requests.get')
def test_get_request_token(mock_get):
    mock_get.return_value.ok = True
    mock_get.return_value.text = 'a=b'

    token = poku.get_response_token('abc')
    assert token == 'b'


@patch('poku.poku.requests.get')
def test_get_request_token_not_ok(mock_get):
    mock_get.return_value.ok = False
    token = poku.get_response_token('abc')
    assert token is None


def test_request_response():
    """ Test pocket endpoint """
    response = requests.get('https://getpocket.com')
    assert response.ok
