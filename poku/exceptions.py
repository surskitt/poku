# -*- coding: utf-8 -*-

""" Custom Exceptions """


class PocketGetRequestTokenException(Exception):
    """ Raise when pocket request token request fails """


class PocketGetAccessTokenException(Exception):
    """ Raise when pocket access token request fails """


class PocketGetItemsException(Exception):
    """ Raise when pocket item pull fails """
