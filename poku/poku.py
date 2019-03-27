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
    parser.add('-c', '--config', is_config_file=True,
               help='config file path')
    parser.add('--consumer', required=True,
               help='pocket consumer key')
    parser.add('--access',
               help='pocket access key')
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

    # retrieve pocket items, ensure unique urls and sort
    pocket_items = [poku.pocket.item_to_dict(i)
                    for i in poku.pocket.get_items(consumer_key, access_token)]
    pocket_items = poku.utils.dict_list_ensure_unique(pocket_items)
    pocket_items = poku.utils.sort_dict_items(pocket_items)

    # retrieve buku items and sort
    bukudb = buku.BukuDb()
    buku_items = [poku.buku.item_to_dict(i) for i in bukudb.get_rec_all()]
    buku_items = poku.utils.sort_dict_items(buku_items)

    # Add new buku items
    new_buku_items = poku.utils.dict_list_difference(pocket_items, buku_items)
    print('Adding {} new items to buku'.format(len(new_buku_items)))
    for bi in new_buku_items:
        bukudb.add_rec(bi['url'], title_in=bi['title'],
                       tags_in=poku.buku.tags_to_tagstring(bi['tags']),
                       immutable=True, delay_commit=True, fetch=False)
    bukudb.conn.commit()
