def sig_first(hub, a, b, c):
    pass


def sig_second(hub, **kwargs):
    pass


def sig_third(hub, a, b, *args, **kwargs):
    pass


def sig_four(hub, a, *args, e=7):
    pass


def sig_five(hub, a, c, *args):
    pass


def sig_six(hub, a, *args, **kwargs):
    pass


def sig_missing():
    '''
    This function is missing in the module to make sure it gets picked up
    '''
    pass
