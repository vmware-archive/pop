# -*- coding: utf-8 -*-
'''
Tools to work with dicts
'''

__virtualname__ = 'dicts'


def traverse(hub, data, key, default=None, delimiter=':'):
    '''
    traverse a dict or list using a colon-delimited (or otherwise delimited,
    using the 'delimiter' param) target string. the target 'foo:bar:0' will
    return data['foo']['bar'][0] if this value exists, and will otherwise
    return the dict in the default argument.
    function will automatically determine the target type.
    the target 'foo:bar:0' will return data['foo']['bar'][0] if data like
    {'foo':{'bar':['baz']}} , if data like {'foo':{'bar':{'0':'baz'}}}
    then return data['foo']['bar']['0']
    '''
    for each in key.split(delimiter):
        if isinstance(data, list):
            try:
                idx = int(each)
            except ValueError:
                embed_match = False
                # Index was not numeric, lets look at any embedded dicts
                for embedded in (x for x in data if isinstance(x, dict)):
                    try:
                        data = embedded[each]
                        embed_match = True
                        break
                    except KeyError:
                        pass
                if not embed_match:
                    # No embedded dicts matched, return the default
                    return default
            else:
                try:
                    data = data[idx]
                except IndexError:
                    return default
        else:
            try:
                data = data[each]
            except (KeyError, TypeError):
                return default
    return data
