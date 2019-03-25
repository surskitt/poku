#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `poku` package."""

import pytest


from poku import poku
import requests


def test_request_response():
    response = requests.get('https://getpocket.com')
    assert response.ok
