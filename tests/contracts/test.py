# -*- coding: utf-8 -*-
'''
Example contract
'''

__virtualname__ = 'test'


def functions(hub):
    '''
    Return the functions
    '''
    return ('ping', 'demo')


def pre_ping(hub, ctx):
    '''
    '''
    print('Calling Pre!')
    if ctx.args:
        raise Exception('ping does not take args!')
    if ctx.kwargs:
        raise Exception('ping does not take kwargs!')


def call_ping(hub, ctx):
    '''
    '''
    print('calling!')
    return ctx.func(*ctx.args, **ctx.kwargs)


def post_ping(hub, ctx):
    '''
    '''
    print('Calling Post!')
    if not isinstance(ctx.ret, dict):
        raise Exception('MUST BE DICT!!')
