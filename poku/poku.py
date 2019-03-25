# -*- coding: utf-8 -*-

"""Main module."""

import configargparse


def parse_args(args):
    conf_files = ['/etc/poku/*.cfg', '~/.config/poku/*.cfg']
    parser = configargparse.ArgParser(default_config_files=conf_files)
    parser.add('--consumer', '-p', required=True)

    return parser.parse_args(args)
