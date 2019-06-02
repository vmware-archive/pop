# -*- coding: utf-8 -*-


__virtualname__ = 'testing'


def call(hub, ctx):
    return 'contract ' + ctx.func(*ctx.args, **ctx.kwargs)


def call_signature_func(hub, ctx):
    args = ctx.get_arguments()
    assert args['param1'] == 'passed in'
    assert args['param2'] == 'default'


async def call_async_echo(hub, ctx):
    return 'async contract ' + await ctx.func(*ctx.args, **ctx.kwargs)
