# -*- coding: utf-8 -*-

""" Main module. """

import sys
import configargparse

import poku


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
    consumer_key = args.consumer

    # retrieve access token if not passed, otherwise use
    if not args.access:
        request_token = poku.pocket.get_request_token(consumer_key)
        auth_url = poku.pocket.generate_auth_url(request_token)
        access_token = poku.pocket.get_access_token(consumer_key,
                                                    request_token)
    else:
        access_token = args.access
