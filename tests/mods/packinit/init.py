# -*- coding: utf-8 -*-
'''
used to test the pack_init system
'''
# pylint: disable=undefined-variable


def __init__(hub):
    '''
    Add a value to the context
    '''
    hub.context['NEW'] = True
    hub.mods._mem['new'] = True


def check(hub):
    return hub.context.get('NEW')
