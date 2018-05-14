# -*- coding: utf-8 -*-
'''
Fail to load to test load errors
'''

__virtualname__ = 'bad'


def __virtual__(hub):
    return 'Failed to load bad'


def func(hub):
    return 'wha?'
