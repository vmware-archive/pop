=======================
Proc Process Management
=======================

The proc system is unlike other process management systems. It is inspired by
the process systems found in Julia and allows for functions to be completly
farmed out to async executions. The proc processes are not forked but are
fresh python executions. These new processes will execute many async python
functions simultaneously.

When sending a fresh command into a proc process just send in the pop reference
and the kwargs, then the function will be started up and the return will be
sent back out to the calling function.

Usage
=====

Start by adding the proc subsystem to your hub (make sure to `init=True`!):

.. code-block:: python

    hub.tools.sub.add('proc', pypath='pop.mods.proc', init=True)

Now the proc subsystem is available. Create a new process pool:

.. code-block:: python

    await hub.proc.init.pool(3, 'Workers')

You now have a worker pool named `Workers` with 3 processes.

Before sending function calls to the pool add a new subsystem to the workers.
Remember that these processes are not forks, they need to have the subsystems
loaded!

Just call `hub.proc.run.add_sub` with the name of the pool as the first argument
followed by the arguments to `tools.sub.add`. Lets add the actor system so we
can get a nice battery of functions to call:

.. code-block:: python

    await hub.proc.run.add_sub('Workers', 'actor', pypath='act.mods.actor', init=True)

The pool can now be sent functions to be run and awaited for. The functions
can be either async functions or just plain python functions. But the real power
of the system is found in sending in async functions.

.. code-block:: python

    ret = await hub.proc.run.func('Workers', 'act.test.ping')

Any args or kwargs passed after the first 2 arguments to hub.proc.run.func will be
passed to the called function.

Generators
==========

Generators and async genrators are also supported, but you need to call a different
function with `proc.run` to return a generator. The function to call is `proc.run.gen`.

Calling this function will always return an async generator, even if the function
called in the proc process is a classic generator, so remember to `async for`, not
just `for`:

.. code-block:: python

    async for ind in hub.proc.run.gen('Workers', 'act.test.iterate'):
        print(ind)

Tracking Calls
==============

Lets say you want the same worker function to be called repeatedly, perhaps
you have a long running async task running that you want to communicate with
by calling more functions. Proc can return the staged coroutine and index of
the intended process to run on!

.. code-block:: python

    ind, coro = await hub.proc.run.track_func('Workers', 'act.test.ping')
    await coro

Now you can send another function in that you know will be run on the same
process as the previous call:

.. code-block:: python

    ret = await hub.proc.run.ind_func('Workers', 1, 'act.test.ping')


Async Callback Server
=====================

Sometimes it may be required to call a function that will return multiple times.
This can be done using a callback function.
