# -*- coding: utf-8 -*-

__virtualname__ = 'priv'


def call(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)
