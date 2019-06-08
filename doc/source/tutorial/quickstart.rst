==========
Quickstart
==========

Using pop to create a plugin oriented project is easy. This tutorial will help you
learn how `pop` works and how to make a project. Once you understand how to build
some basic tools in `pop` you can use the `pop-seed` tool to make setting up new
projects easy.

Start by making a new directory for your project:

.. code-block:: bash

    mkdir poppy

Now create a simple python script called *run.py* to create the `hub` and start the
plugin system.

The `hub` is the root of the namespace that `pop` opperates on. Don't worry, it is not
that complicated! Think of the hub like a big `self` variable that is shared accross
your entire application. The hub allows you to save data that is relative to your plugins
while still allowing that data to be shared safely accross the appication.

.. code-block:: python

    import pop.hub

    # Create the hub
    hub = pop.hub.Hub()
    # Load up your first plugin subsystem called "plugins"
    hub.tools.sub.add('poppy.plugins')

This script has created your `hub` and loaded up your first subsystem, or `sub`. The
`pypath` option tells `pop` where to load up the python package that contains the plugins.
So lets create the python package and make it start to work! Make a new directory
called poppy as the base python package and then another for your plugins.

.. code-block:: bash

    mkdir -p poppy/plugins

Now that you are in the new poppy directory create the new plugin subsystem's initializer.
Create a file called *poppy/plugins/init.py* and give it an `__init__` function. Like a
class you can initialize a new plugin subsystem, or a new module.

.. code-block:: python

    def __init__(hub):
        print('Hello World!!')

Now that you have a plugin with an initializer you can run it! Go back to the same directory
as the *run.py* file and execute it.

.. code-block:: bash

    python3 run.py

With a project up and running you can now add more plugins, more code and more subsystems!

Adding Configuration Data
=========================

Now that you have the basic structure of your application you can easily add configuration
data to your project.

Loading configuration data into a project looks easy at first but quickly becomes difficult.
To solve this issue `pop` comes with a system to make configuration loading easy.

When loading configuration data, the data can come from many sources, the command line,
environment variables, windows registery, configuration files, etc. But certian sources
should overwrite other sources; config files overwrite defaults, environment variables overwrite
config files and cli overwrites all. Also, you end up defining default configuration values
and paramaters in multiple places to enable supporting multiple mediums for configuration input.
Finally, you only want to have to document your configuration options in one place.

The `conf` system in `pop` solves this issue by making a single location where you can
define your configuration data. You can also merge the configuration data from multiple `pop`
projects, just like you can add other `pop` projects' plugin subsystems to your project's `hub`!

Using the `conf` system, is easy! Create a file called `poppy/config.py` and populate it with
your configuration data.

.. code-block:: python

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

Now lets change the `__init__` function in *poppy/plugins/init.py* to load up the project's config!

.. code-block:: python

    def __init__(hub):
        hub.tools.conf.integrate(['poppy'], loader='yaml', roots=True)

Now the configuration data has been loaded, if you run poppy with `--help` you will see
all of your configuration options available. The configuration options will now be made
available on the `hub` under the `OPT` dict and under the name of the imported project.

This allows for configuration data to be loaded from multiple projects and still cleanly
namespaced. So the values of our configurations will be available on the `hub`:

.. code-block:: python

    hub.OPT['poppy']['addr']
    hub.OPT['poppy']['port']

Take a look at the documentation on the conf system to better understand what options are
available and how to use some of the more powerfull systems.

Adding More Plugin Subsystems
=============================

Next lets create a new plugin subsystem. This makes a new namspace on the hub and allows us
to create a pattern in `pop`. So there are a few more new terms to learn!

A plugin subsystem is typically refered to as a `sub`. This is a namespace on the `hub` that
defines the new set of plugins. Using these namespaces on the `hub` allows you to set variables
on the `hub` that are defined as to how they should be used based on where they exist. Data
on the hub should only be written by relative plugins, but can be read globally.

When you create a new `sub` it should follow a `pattern`. These patterns define how the `sub`
interacts with your application. We will start by making a simple `pattern` called the
`library pattern`. This pattern means that modules have functions that are generally available.

When the `hub` is created it comes with a `sub` called `tools`. The `tools` `sub` comes with
the functions we need to add our own `hub`. Now you can execute `hub.tools.sub.add` to add a new
plugin subsystem:

.. code-block:: python

    def __init__(hub):
        hub.tools.conf.integrate(['poppy'], loader='yaml', roots=True)
        hub.tools.sub.add('rpc', pypath='poppy.rpc')

Now that we are able to load up a new subsystem we need to define it in our code! Start by making
a new directory inside of `poppy/` called `rpc`. When we added the new `sub` we named it `rpc`
and we specified the path to find the `rpc` `sub` to be in the `poppy.rpc`.

Now create the *poppy/rpc/init.py* file and make an rpc server. This rpc server will expose
all of the functions in the `rpc` plugin subsystem over a simple http server.

.. code-block:: python

    def __init__(hub):
        # Make a simplehttp rpc server
