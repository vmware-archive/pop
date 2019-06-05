==========
Quickstart
==========

Using pop to create a plugin oriented project is easy. Pop comes with a simple script to build
the basic parts of a pop project. The `pop-seed` script builds the directory structure and
adds a setup.py that autodetects all new plugins and a script for your new project.

Just pick a directory to start in and run `pop-seed`:

.. code-block:: bash

    pop-seed poppy

This command will make a new project called poppy, the setup.py, requirements.txt, a
script to run the project and the directories to hold your first plugin subsystem.

With these assets at hand you can run the application however you please, via system
installation, pyvenv, docker etc.

In the scripts directory you will find a script called `poppy`. If you open it up you
will see the simple creation of a pop project. The creation of the hub, and the setup of
the first plugin subsystem. As well as the call to run the first code.

The first code to run is in the file `poppy/mods/poppy/init.py`. There you will find
the `new` function. The `new` function is used to initialize a plugin subsystem when needed.

Next open up the poppy subsystem's `init.py` file:

`poppy/mods/poppy/init.py`:


.. code-block:: python

    def new(hub):
        print('poppy works')


The `pop-seed` application has created something that is very central to the Plugin Oriented Programming
design, the `hub`.

The `hub` is the root of the namespace that `pop` opperates on. Don't worry, it is not
that complicated! Think of the hub like a big `self` variable that is shared accross
your entire application. The hub allows you to save data that is relative to your plugins
while still allowing that data to be shared safely accross the appication.

With a project up and running you can now add more plugins, more code and more subsystems!

Adding Configuration Data
=========================

Once you have the basic structure of your application build out for you by `pop-seed`,
you can easily add configuration data to your project.

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

Using the `conf` system, is easy! When you ran `pop-seed` the first time it created a file called
`poppy/config.py`.

Open up that file and add some configuration options:


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
    CONFIG = {}
    GLOBAL = {}
    SUBS = {}

Now lets change the `hub.poppy.init.new` function to load up the project's config!

.. code-block:: python

    def new(hub):
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

    def new(hub):
        hub.tools.conf.integrate(['poppy'], loader='yaml', roots=True)
        hub.tools.sub.add('rpc', pypath='poppy.mods.rpc')

Now that we are able to load up a new subsystem we need to define it in our code! Start by making
a new directory inside of `poppy/mods` called `rpc`. When we added the new `sub` we named it `rpc`
and we specified the path to find the `rpc` `sub` to be in the `poppy.mods.rpc`.
