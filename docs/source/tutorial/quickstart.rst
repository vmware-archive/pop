==========
Quickstart
==========

Using pop to create a plugin oriented project is easy. This tutorial will help you
learn how `pop` works and how to make a project. Once you understand how to build
some basic tools in `pop` you can use the `pop-seed` tool to make setting up new
projects easy.

Getting Started
===============

Start by making a new directory for your project:

.. code-block:: bash

    mkdir poppy

Now create a simple python script called *run.py* to create the `hub` and start the
plugin system.

.. note::

    Normally a python project uses `setuptools` and a setup.py file. Because this tutorial
    is about `pop` we skip this part and use the *run.py* script. This can make development
    easier because you can run your application directly from your checkout.
    `pop` ships with a program called `pop-seed` that makes these files and a stock setup.py
    file for you for development convenience! But this tutorial is about learning, so save
    the `pop-seed` script for when you better know `pop`!

The `hub` is the root of the namespace that `pop` operates on. Don't worry, it is not
that complicated! Think of the hub like a big `self` variable that is shared across
your entire application. The hub allows you to save data that is relative to your plugins
while still allowing that data to be shared safely across the application.

.. code-block:: python

    # poppy/run.py

    import pop.hub

    # Create the hub
    hub = pop.hub.Hub()
    # Load up your first plugin subsystem called "plugins"
    hub.pop.sub.add('poppy.poppy')

This script has created your `hub` and loaded up your first subsystem, or `sub`. The
`pypath` option tells `pop` where to load up the python package that contains the plugins.

.. note::

    To learn more about the `hub` take a look at our doc on the hub and how to use it:
    :ref:`hub_overview`

Now lets create the python package and make it start to work! Make a new directory
called poppy as the base python package and then another for your plugins.

.. code-block:: bash

    mkdir -p poppy/poppy

Now that you are in the new poppy directory create the new plugin subsystem's initializer.
Create a file called *poppy/poppy/init.py* and give it an `__init__` function. Like a
class you can initialize a new plugin subsystem, or a new module.

.. code-block:: python

    # poppy/poppy/init.py

    def __init__(hub):
        print('Hello World!!')

.. note::

    Your first `sub` has been created! To learn more about making subs check the doc here:
    :ref:`subs_overview`

Now that you have a plugin with an initializer you can run it! Go back to the same directory
as the *run.py* file and execute it.

.. code-block:: bash

    python3 run.py

With a project up and running you can now add more plugins, more code and more subsystems!

.. note::

    When you make a new sub that sub follows a `pattern`. Patterns are an important part of
    Plugin Oriented Programming. Get to know the basics first! But then spend a few minutes
    learning about `patterns` here: :ref:`sub_patterns`. Just so you know, the pattern you
    just started is called the **spine** pattern.

Adding Configuration Data
=========================

Now that you have the basic structure of your application you can easily add configuration
data to your project.

Loading configuration data into a project looks easy at first but quickly becomes difficult.
To solve this issue `pop` comes with a system to make configuration loading easy.

When loading configuration data, the data can come from many sources, the command line,
environment variables, windows registry, configuration files, etc. But certain sources
should overwrite other sources; config files overwrite defaults, environment variables overwrite
config files and cli overwrites all. Also, you end up defining default configuration values
and parameters in multiple places to enable supporting multiple mediums for configuration input.
Finally, you only want to have to document your configuration options in one place.

The `conf` system in `pop` solves this issue by making a single location where you can
define your configuration data. You can also merge the configuration data from multiple `pop`
projects, just like you can add other `pop` projects' plugin subsystems to your project's `hub`!

.. note::

    That's right! I just said that you can merge entire applications together onto one hub and
    bring in all the configuration data too! To learn more about his take a look at the doc
    on merging applications: :ref:`app_merging`

Using the `conf` system, is easy! Create a file called `poppy/conf.py` and populate it with
your configuration data.

.. code-block:: python

    # poppy/conf.py

    CLI_CONFIG = {
            'addr': {
                'options': ['-a'],
                'default': '127.0.0.1',
                'help': 'The address to present the rpc server on',
                },
            'port': {
                'options': ['-p'],
                'default': 8888,
                'help': 'The port to bind to',
                },
            }

Now lets change the `__init__` function in *poppy/poppy/init.py* to load up the project's config!

.. code-block:: python

    # poppy/poppy/init.py

    def __init__(hub):
        hub.pop.conf.integrate(['poppy'], loader='yaml', cli='poppy', roots=True)

Now the configuration data has been loaded, if you run *run.py* with `--help` you will see
all of your configuration options available. The configuration options will now be made
available on the `hub` under the `OPT` dict and under the name of the imported project.

This allows for configuration data to be loaded from multiple projects and still cleanly
namespaced. So the values of our configurations will be available on the `hub`:

.. code-block:: python

    hub.OPT['poppy']['addr']
    hub.OPT['poppy']['port']

.. note::

    The `conf` system is very powerful and expansive, take a look at the docs on the conf
    system to get to know more of the available options and features. It is made to solve
    many problems that occur when loading configuration data:
    :ref:`conf_overview`
    :ref:`conf_integrate_overview`

Adding More Plugin Subsystems
=============================

Next lets create a new plugin subsystem. This makes a new namespace on the hub and allows us
to create a pattern in `pop`. So there are a few more new terms to learn!

A plugin subsystem is typically referred to as a `sub`. This is a namespace on the `hub` that
defines the new set of plugins. Using these namespaces on the `hub` allows you to set variables
on the `hub` that are defined as to how they should be used based on where they exist. Data
on the hub should only be written by relative plugins, but can be read globally.

.. note::

    Remember how I mentioned patterns before? If you are curious, the sub we are making now
    follows the `router` pattern. :ref:`sub_patterns`

When you create a new `sub` it should follow a `pattern`. These patterns define how the `sub`
interacts with your application. We will start by making a simple `pattern` called the
`library pattern`. This pattern means that modules have functions that are generally available.

When the `hub` is created it comes with a `sub` called `pop`. The `pop` `sub` comes with
the functions we need to add our own `hub`. Now you can execute `hub.pop.sub.add` to add a new
plugin subsystem:

.. code-block:: python

    def __init__(hub):
        hub.pop.conf.integrate(['poppy'], loader='yaml', roots=True)
        hub.pop.sub.add(pypath='poppy.rpc')

Now that we are able to load up a new subsystem we need to define it in our code! Start by making
a new directory inside of `poppy/` called `rpc`. When we added the new `sub` we specified the path
to find the `rpc` `sub` to be in the `poppy.rpc`.

Now create the *poppy/rpc/init.py* file and make an rpc server. This rpc server will expose
all of the functions in the `rpc` plugin subsystem over a simple http server.

.. code-block:: python

    from aiohttp import web

    def __init__(hub):
        app = web.Application()
        app.add_routes([web.get('/', hub.rpc.init.router)])
        web.run_app(app)

    async def router(hub, request):
        data = request.json()
        if 'ref' in data:
            return web.json_response(getattr(hub.rpc, data['ref'])(**data.get('kwargs')))

Congratulations! You now have a working rpc server that takes json requests and routes to
plugins in the `rpc` sub. Now we just need to make a module in the `rpc` sub to route the
requests to, lets call this file *poppy/rpc/math.py*:

.. code-block:: python

    async def fib(hub, num=10):
        num = int(num)
        if num < 2:
            return num
        prev = 0
        curr = 1
        i = 1
        while i < num:
            prev, curr = curr, prev + curr
            i += 1
        return curr

Now your rpc server can compute the Fibonacci sequence. So lets start up the server with the
*run.py* script and then hit it with a curl command:

.. code-block:: bash

    python3 run.py

.. TODO: Look up the curl command to use and verify this code

Now that you have a project up and running you can play around with extending what `pop` can
do and get familiar with it.


Docs Review
===========

In this doc we introduced a lot of concepts, this is a whole new programming paradigm!
To become more familiar with Plugin Oriented Programming and `pop` we already introduced these
docs:

What is a hub and how to use it:
    :ref:`hub_overview`

What a sub is and how to use it:
    :ref:`subs_overview`

What patters are and some examples of patterns that can help you start thinking in `pop`
    :ref:`sub_patterns`

How the built in configuration loading system `conf` works:
    :ref:`conf_overview` and
    :ref:`conf_integrate_overview`

How the concept of app merging works:
    :ref:`app_merging`

Next Steps
==========

Now that you have the tools you need to make `pop` work you will be able to start understanding
how to think in and really use the power behind Plugin Oriented Programming! Take a look at these
docs to get a better overview of Plugin Oriented programming:

Learning Plugin Oriented Programming
====================================

Learning and thinking in Plugin Oriented Programming starts here, it is a short doc trying to outline
how to think about your applications so they can all be truly Plugin Oriented:
:ref:`learning_POP`

The Story Behind Plugin Oriented Programming
============================================

Plugin Oriented Programming deviates from many of the norms in software development while working
to evolve to the modern way of developing. Learn about Thomas Hatch and how he came up with
the Plugin Oriented Programming paradigm:
:ref:`story_of_pop`
