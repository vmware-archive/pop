# -*- coding: utf-8 -*-
'''
Contract Context
'''

__virtualname__ = 'ctx_update'


def pre(hub, ctx):
    '''
    '''
    assert ctx.args == [hub, True]
    # Let's replace the context arguments
    ctx.args[1] = False
    assert ctx.args == [hub, False]


def call_test_call(hub, ctx):
    '''
    '''
    assert ctx.args == [hub, False]
    return 'contract executed'


def post(hub, ctx):
    '''
    '''
    assert ctx.args == [hub, False]
    return ctx.ret
