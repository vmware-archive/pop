'''
The Proc sub is used to spin up worker processes that run hub referenced
coroutines.
'''
# Import python libs
import os
import sys
import atexit
import itertools
import asyncio
import subprocess


def new(hub):
    '''
    Create constants used by the client and server side of procs
    '''
    hub.proc.DELIM = b'f1d219f8c8c01f11'
    hub.proc.Workers = {}
    hub.proc.WorkersIter = {}


def _get_cmd(hub, ref):
    '''
    Return the shell command to execute that will start up the worker
    '''
    code = 'import sys; '
    code += 'import pop.hub; '
    code += 'hub = pop.hub.Hub(); '
    code += 'hub.tools.sub.add("proc", pypath="pop.mods.proc", init=True); '
    code += 'hub.proc.worker.start("{}", "{}")'.format(hub.opts['sock_dir'], ref)
    cmd = '{} -c \'{}\''.format(sys.executable, code)
    return cmd


def mk_proc(hub, ind, workers):
    '''
    Create the process and add it to the passed in workers dict at the
    specified index
    '''
    ref = os.urandom(3).hex() + '.sock'
    workers[ind] = {'ref': ref}
    workers[ind]['path'] = os.path.join(hub.opts['sock_dir'], ref)
    cmd = _get_cmd(hub, ref)
    workers[ind]['proc'] = subprocess.Popen(cmd, shell=True)
    workers[ind]['pid'] = workers[ind]['proc'].pid


async def local_pool(hub, num, name='Workers'):
    '''
    Create a new local pool of process based workers

    :param num: The number of processes to add to this pool
    :param ref: The location on the hub to create the Workers dict used to
        store the worker pool, defaults to `hub.tools.proc.Workers`
    '''
    if not hub.proc.Tracker:
        hub.proc.init.mk_tracker()
    workers = {}
    for ind in range(num):
        hub.proc.init.mk_proc(ind, workers)
    w_iter = itertools.cycle(workers)
    hub.proc.Workers[name] = workers
    hub.proc.WorkersIter[name] = w_iter
    # TODO: This seems to be spawning extra procs, this should be fixed
    #asyncio.ensure_future(hub.proc.init.maintain(name))


async def maintain(hub, name):
    '''
    Keep an eye on these processes
    '''
    workers = hub.proc.Workers[name]
    while True:
        for ind, data in workers.items():
            if not data['proc'].poll():
                hub.proc.init.mk_proc(ind, workers)
        await asyncio.sleep(2)


def mk_tracker(hub):
    '''
    Create the process tracker, this simply makes a data structure to hold
    process references and sets them to be terminated when the system is
    shutdown.
    '''
    hub.proc.Tracker = True
    atexit.register(hub.proc.init.clean)


def clean(hub):
    '''
    Clean up the processes registered in the tracker
    '''
    print('Cleaning Procs!')
    for name, workers in hub.proc.Workers.items():
        print(name)
        print(workers)
        for ind in workers:
            workers[ind]['proc'].terminate()
