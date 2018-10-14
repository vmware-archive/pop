'''
Some test interfaces to show how to use dflow and allow tests to run
'''


async def echo_router(hub, pool_name, cname, data):
    '''
    An example router used in tests
    '''
    ret = {}
    if 'stag' in data:
        rtag = data['stag']
    else:
        rtag = None
    msg = data['msg']
    await hub.com.con.send(pool_name, cname, msg, rtag)
