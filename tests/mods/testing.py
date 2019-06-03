# -*- coding: utf-8 -*-

'''
module used while testing mock hubs provided in 'testing'.
'''


__contracts__ = ['testing']


def noparam(hub):
    pass


def echo(hub, param):
    return param


def signature_func(hub, param1, param2='default'):
    pass


def attr_func(hub):
    pass


attr_func.test = True
attr_func.__test__ = True


async def async_echo(hub, param):
    return param
