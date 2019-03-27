# -*- coding: utf-8 -*-

""" buku specific functions """


def item_to_dict(b_item):
    """ convert buku item to universal dict """
    out = {
        'url': b_item[1],
        'title': b_item[2],
        'tags': sorted(b_item[3].split(',')[1:-1]),
        'timestamp': b_item[0]
    }

    return out


def tags_to_tagstring(tag_list):
    """ convert list of tags to tagstring """
    if tag_list == []:
        return ','

    return ',{},'.format(','.join(tag_list))
