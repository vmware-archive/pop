===============
Getting Started
===============

We will make a simple application called `poppy` to expose an RPC interface over a websocket.
This will introduce you to a number of plugin subsystem patterns in `pop` and
introduce you to the core concepts of the platform and some of the core libraries.


Create the Project Structure
============================

There are only a few things you need to know to get started with `pop`. We can
easily start on the creation of the `hub`. These first steps can be done with
the `pop_seed` script, but for completeness they will be covered here. If
you used the quickstart guide or the `pop_seed` script, then you can skip to
the next section. When normally starting a `pop` project it is suggested you use
`pop_seed` as it gives you a lot more than you get in this brief intro.

Start by making some directories. In `pop` you first need to make a hub. This
is the only code that is not a plugin. Since it is only a few lines you can
still call an application 100% pluggable.

Start by making a directory called `scripts` and adding a file called `poppy`:

.. code-block:: python

    import pop.hub

    hub = pop.hub.Hub()
    hub.tools.sub.add('poppy', pypath='poppy.mods.poppy', init=True)


In this code you import pop, create the hub and add your first sub. The `pypath` argument
points to where the plugins are stored. When making a pop program place the `modules` under
mods and the `contracts` under contracts inside the python package. In this case the pypath
`poppy.mods.poppy` refers to the path python finds when importing `poppy.mods.poppy`. Now
`pop` will populate the plugin subsystem with files from that path. The argument `init=True`
means that when once the plugin system is started it will run the `init.new` function in
the newly created sub. So lets put some plugins in the there!

Start by making the diectories:

.. code-block:: bash

    touch poppy/__init__.py poppy/mods/__init__.py poppy/mods/poppy/__init__.py

Now open up the `init.py` file in the poppy subsystem. Don't confuse the `init.py` file with
the `__init__.py` files. The `__init__.py` files should always be left empty!

poppy/mods/poppy/init.py:

.. code-block:: python

    def new(hub):
        print('Poppy works!')



Bring in Configuration Data
===========================

Since this is a full blown application, we should start with loading some configuration options.
When loading configuration options there is a problem, you want a config file, and cli options.
But you also want to load the arguments in the right order, for instance you want
