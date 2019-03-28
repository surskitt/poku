#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for buku functions. """

import pytest

import poku


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
