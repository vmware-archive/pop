'''
Define the hub, the core object used by pop
'''


class Hub:
    '''
    The Hub object is used as the root object for a pop system. This object
    is intended to be the root of all interaction with other plugin systems
    '''
    def __init__(self):
        self._subs = {}

    def __getattr__(self, item):
        '''
        '''
        if item in self._subs:
            return self._subs[item]
        raise ValueError(item)
