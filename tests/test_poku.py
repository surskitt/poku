#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `poku` package."""

import pytest


from poku import poku
import requests
import configargparse


def test_parse_consumer():
    args = poku.parse_args(['--consumer', 'abc'])
    assert args.consumer == 'abc'


def test_no_consumer():
    with pytest.raises(SystemExit):
        args = poku.parse_args([])


def test_request_response():
    response = requests.get('https://getpocket.com')
    assert response.ok
