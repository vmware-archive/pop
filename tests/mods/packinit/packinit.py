# -*- coding: utf-8 -*-
# pylint: disable=undefined-variable


def __mod_init__(hub):
    hub.context['LOADED'] = True


def loaded(hub):
    return 'LOADED' in hub.context
