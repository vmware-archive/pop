# Import python libs
import asyncio

__virtualname__ = 'cmd'


async def stdout(hub, cmd):
    '''
    Run the passed in function and return the standard out
    '''
    proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            )
    while True:
        line = await proc.stdout.readline()
        if not line:
            break
        yield line
    await proc.wait()
