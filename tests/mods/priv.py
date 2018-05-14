# -*- coding: utf-8 -*-


def public(hub):
    return _private(hub)


def _private(hub):
    return hub.opts  # pylint: disable=undefined-variable
