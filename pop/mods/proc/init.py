'''
The Proc sub is used to spin up worker processes that run hub referenced
coroutines.
'''
# Import python libs
import sys
import asyncio


def _get_cmd():
    '''
    Return the shell command to execute that will start up the worker
    '''
    code = 'import sys; import pop.hub; sys.path={}; pop.hub.Hub().tools.sub.add("proc", "pop.mods.proc", init=True)'.format(sys.path)
    cmd = '{} -c {}'.format(sys.executable, code)


def worker(hub):
    '''
    This funtion is called by the startup script to create a worker process

    :NOTE: This is a new process started from the shell, it does not have any
    of the process namespace from the creating process.
    This is an EXEC, NOT a FORK!
    '''
    # Create io loop
    # Create server
    # Accept calls and execute


async def local_pool(hub, num, ref='hub.tools.proc.Workers'):
    '''
    Create a new local pool of process based workers

    :param num: The number of processes to add to this pool
    :param ref: The location on the hub to create the Workers dict used to
        store the worker pool, defaults to `hub.tools.proc.Workers`
    '''
    workers = {}
    hub.tools.ref.create(ref, workers)
    for ind in range(num):
        workers[ind] = {}
        cmd = _get_cmd()
        workers[ind]['proc'] = await asyncio.create_subprocess_shell(cmd)
