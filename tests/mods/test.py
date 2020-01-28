# -*- coding: utf-8 -*-

# Import python libs
import os

# Import pack libs
import pytest

from pop.scanner import scan  # pylint: disable=unused-import

__virtualname__ = 'test'
__contracts__ = 'test'
__func_alias__ = {'ping_': 'ping'}


def ping_(hub):
    return {}


def demo(hub):
    return False


def this(hub):
    return hub._.ping()


def fqn(hub):
    return hub.mods.test.ping()


def module_level_non_aliased_ping_call(hub):
    return ping_()  # pylint: disable=no-value-for-parameter


def module_level_non_aliased_ping_call_fw_hub(hub):
    return ping_(hub)


def attr():
    return True


attr.bar = True


def call_scan(hub):
    # If scan has been packed(wrongly), the call below will throw a TypeError because
    # we'll also pass hub
    scan([os.path.dirname(__file__)])
    return True


def double_underscore(hub):
    assert hub.__ is hub.mods
    assert hub.___ is hub
    assert hub.______ is hub
