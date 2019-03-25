#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `poku` package."""

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


def test_request_response():
    """ Test pocket endpoint """
    response = requests.get('https://getpocket.com')
    assert response.ok
