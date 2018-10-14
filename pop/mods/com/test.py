'''
Some test interfaces to show how to use dflow and allow tests to run
'''


async def echo_router(hub, ctx, msg):
    '''
    An example router used in tests
    '''
    return msg
