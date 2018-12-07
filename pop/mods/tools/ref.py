'''
Used to resolve resolutions to paths on the hub
'''


def last(hub, ref):
    '''
    Takes a string that references the desired ref and returns the last object
    called out in that ref
    '''
    return hub.tools.ref.path(ref)[-1]


def path(hub, ref):
    '''
    Retuns a list of references up to the named ref
    '''
    ret = [hub]
    if isinstance(ref, str):
        ref = ref.split('.')
    for chunk in ref:
        ret.append(getattr(ret[-1], chunk))
    return ret


def create(hub, ref, obj):
    '''
    Create an attribute at a given target using just a ref string and the
    object to be saved at said location. The desired location must already
    exist!

    :param ref: The dot delimited string referencing the target location to
        create the given object on the hub
    :param obj: The object to store at the given reference point
    '''
    comps = ref.split('.')
    sub_ref = ref[:ref.rindex('.')]
    var = comps[-1]
    top = hub.tools.ref.last(sub_ref)
    setattr(top, var, obj)
