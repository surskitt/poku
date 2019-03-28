#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for general utility functions. """

import pytest

import poku


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
