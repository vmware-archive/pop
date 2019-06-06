# -*- coding: utf-8 -*-
# pylint: disable=undefined-variable


def __init__(hub):
    hub.context['LOADED'] = True


def loaded(hub):
    return 'LOADED' in hub.context
