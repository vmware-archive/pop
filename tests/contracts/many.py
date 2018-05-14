# -*- coding: utf-8 -*-

__virtualname__ = 'all'


def pre(hub, ctx):
    if len(ctx.args) > 1:
        raise ValueError('No can haz args!')
    if ctx.kwargs:
        raise ValueError('No can haz kwargs!')


def call(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_list(hub, ctx):
    return ['override']


def post(hub, ctx):
    ret = ctx.ret
    if isinstance(ret, list):
        ret.append('post called')
    elif isinstance(ret, dict):
        ret['post'] = 'called'
    return ret
