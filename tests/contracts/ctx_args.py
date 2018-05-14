# -*- coding: utf-8 -*-
'''
Contract Context
'''

__virtualname__ = 'ctx_args'


def call(hub, ctx):
    '''
    '''
    return ctx.get_argument(ctx.get_argument('value'))
