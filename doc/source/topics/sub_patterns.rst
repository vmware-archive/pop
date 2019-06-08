==================
Subsystem Patterns
==================

When making subsystems the best thing to do is make sure that the subsystem follows a pattern.
Patterns are the model for how a subsystem is used. When a pattern is used then all of the plugins
in the subsystem do similar tasks and follow similar models. Some patterns are good at specific
tasks, such as an rpc/rest backend. Some patterns are good at disparate tasks, like setting up
and running a server.

This document covers a number of common patterns, but you can create new patterns! Just make
sure that your pattern is well documented and contracted.

Spine Pattern
=============

The spine pattern is very common, because it defines the startup spine of an application. This
is a pattern where your application loads up config data, starts worker processes and loads the
bulk of the subsystems to be used.

The spine is typically the first subsystem loaded from the startup script. The spine should
be very small and only have a few plugins. Try to keep the spine very limited, and just
enough to start the application. The spine typically runs the following things:

* Set up the core data structures used by the application
* Load up `conf` and read in the application configuration
* Load up additional subsystems
* Start up an asyncio loop
* Start the main coroutines or functions

Beacon Pattern
==============

The name of the beacon pattern comes from Salt's Beacon system. Salt's Beacon system starts
one coroutine per plugin module. In this example we will make a simple cryptocurrency tracker.
This would be a simple *init.py*:

.. code-block:: python

    async def start(hub):
        '''
        Start the beacon listening process
        '''
        gens = []
        for mod in hub.beacons:
            if not hasattr(mod, 'listen'):
                continue
            func = getattr(mod, 'listen')
            gens.append(func())
        async for ret in hub.tools.loop.as_yielded(gens):
            await hub.beacons.QUE.put(ret)

This example shows iterating over the modules found in the beacons sub. The plugins are
defined as needing to impliment an async generator function. We call the async generator
function, which returns an async generator that gets appended to a list. That list is then
passed to the as_yielded fucntion that yields as the next async generator yields. The
yielded data is then added to a QUE that can be ingested elsewhere.

Following this patern a plugin that emits a beacon would subsequently look like this:

.. code-block:: python

    import asyncio
    import aiohttp

    async def listen(hub):
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.cryptonator.com/api/full/btc-usd') as resp:
                    yield(resp.json())
            await asyncio.sleep(5)

Now we have a bitcoin ticker. More modules could act as means to gather data about other
cryptocurrencies.

Collection Pattern
==================

The collection pattern is where an expansive number of modules can be added that define the
on demand collection of data. A good example here is to collect system information. This
makes it simple to extend what data is being gathered and to support more platforms.

A simple example of a collection pattern *init.py* file could look like this:

.. code-block:: python

    import asyncio

    async def run(hub):
        '''
        Run the data collection
        '''
        hub.system.DATA = {}
        coros = []
        for mod in hub.system:
            if not hasattr(mod, 'gather'):
                continue
            func = getattr(mod, 'gather')
            ret = func()
            if asyncio.iscoroutine(ret):
                coros.append(ret)
        await asyncio.gather(coros)

This example allows for plugin modules to create both functrions and async functions and
execute the async functions in paralell. A simple module for this example of the collection
patter could look like this plugin called *os.py*:

.. code-block:: python

    import sys

    def gather(hub):
    if sys.platform.startswith('win'):
        hub.system.DATA['kernel'] = 'windows'
    elif sys.platform.startswith('linux'):
        hub.system.DATA['kernel'] = 'linux'
    elif sys.platform.startswith('darwin'):
        hub.system.DATA['kernel'] = 'darwin'

The collection pattern we used here allowed the modules to populate a dict on the hub. But
we could have just as easily returned the data we wanted to put on the hub and had the
function in the *init.py* aggregate the data.