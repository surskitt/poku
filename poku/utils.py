# -*- coding: utf-8 -*-

""" General util functions """

import configargparse


def parse_args(args):
    """ parse arguments using configargparse module """
    conf_files = ['/etc/poku/*.cfg', '~/.config/poku/*.cfg']
    parser = configargparse.ArgParser(default_config_files=conf_files)
    parser.add('--consumer', required=True)
    parser.add('--access')
    args = parser.parse_args(args)

    return args


def sort_dict_items(item_list):
    """ sort list of dict items based on update time """
    return sorted(item_list, key=lambda x: x['timestamp'])


def dict_list_difference(l1, l2):
    """ return items in l1 but not in l2 """
    return [i for i in l1 if i['url'] not in [j['url'] for j in l2]]
