# -*- coding: utf-8 -*-

""" General util functions """


def sort_dict_items(item_list):
    """ sort list of dict items based on update time """
    return sorted(item_list, key=lambda x: x['timestamp'])


def dict_list_difference(l1, l2):
    """ return items in l1 but not in l2 """
    return [i for i in l1 if i['url'] not in [j['url'] for j in l2]]


def dict_list_ensure_unique(item_list):
    """ ensure all items in list have a unique url (newer wins) """
    return list({i['url']: i for i in item_list}.values())
