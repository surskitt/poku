# -*- coding: utf-8 -*-

""" Main module. """

import sys
import configargparse


def parse_args(args):
    """ parse arguments using configargparse module """
    conf_files = ['/etc/poku/*.cfg', '~/.config/poku/*.cfg']
    parser = configargparse.ArgParser(default_config_files=conf_files)
    parser.add('--consumer', required=True)
    parser.add('--access')
    args = parser.parse_args(args)

    return args


def main():
    args = parse_args(sys.argv[1:])


if __name__ == '__main__':
    main()
