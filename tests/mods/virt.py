# -*- coding: utf-8 -*-


def __virtual__(hub):
    '''
    '''
    try:
        hub.opts  # pylint: disable=undefined-variable
    except Exception:  # pylint: disable=broad-except
        return False
    return True


def present(hub):
    return True
