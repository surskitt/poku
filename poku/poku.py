# -*- coding: utf-8 -*-

""" Main module. """

import sys
import configargparse
import webbrowser
import buku

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
        print('Opening {} in browser'.format(auth_url))
        webbrowser.open(auth_url)
        input('Press Enter here once auth request is approved')
        access_token = poku.pocket.get_access_token(consumer_key,
                                                    request_token)
        print('Access token: {}'.format(access_token))
        print('Pass as argument or add to config to avoid this step in future')
    else:
        access_token = args.access


