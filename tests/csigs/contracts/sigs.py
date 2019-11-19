# Import python libs
from typing import List

def sig_first(hub, a: str, b, c: List):
    pass


def sig_second(hub, **kwargs):
    pass


def sig_third(hub, a, b, *args, **kwargs):
    pass


def sig_four(hub, a, *args, e=7):
    pass


def sig_five(hub, a: str, *args):
    pass


def sig_six(hub, a, *args, **kwargs):
    pass


def sig_seven(hub, foo):
    pass


def sig_missing():
    '''
    This function is missing in the module to make sure it gets picked up
    '''
    pass
