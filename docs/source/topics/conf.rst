.. _conf_overview:

=====================
Configuration Reading
=====================

One of the classic issues with systems software development is adding
configuration and options to CLI programs. The problem is that configuration
data needs to come from multiple sources. Defaults need to be set, CLI options
need to be accepted, config file(s) needs to exist. Config file settings need to
override defaults, while CLI options need to override both, but the CLI needs
to be able to define the location of the config file(s). Finally there ends up
being multiple sources of truth. Config options are documented in one place
while config file options are documented elsewhere.

This little issue can get confusing, and turns into a manual process for many
applications. Pop's `conf` subsystem aims to solve this problem! Instead of
having to maintain multiple sources of documentation, it is in one place. Instead
of having to build the system that takes care of these deps, it is in one place.
Instead of defining all of the loading of config files `conf` supports multiple
file formats.

All in all, `conf` should make your life much easier!

Getting Started
===============

To use `conf` start by adding the `conf` subsystem to your hub:

.. code-block:: python

    hub.tools.sub.add('pop.mods.conf')

Next create a python dict with your configuration data, we will start with something simple:

.. code-block:: python

    CONFIG = {
        'cache_dir': {
            'default': '/var/cache/',
            'help': 'The place to cache stuff!',
            },
        }

Now with a configuration dict you can call `conf.reader.read` on it:

.. code-block:: python

    hub.OPTS = hub.conf.reader.read(CONFIG)

Following `pop` conventions it would make sense to save your configuration
values on the hub so they are available to your application.

.. note::
    Typically loading configuration is done at the beginning of an application. A good place therefore
    to load up configs could be as early as in the primary init.new function in your first subsystem.

Adding Extra CLI Options
========================

The CLI option is determined by the top level dict key, but often it is preferred
to add an alternative or a shortcut option to the CLI, this can be easily added:

.. code-block:: python

    CONFIG = {
        'cache_dir': {
            'options': ['-C', '--cacheland'],
            'default': '/var/cache/',
            'help': 'The place to cache stuff!',
            },
        }

Actions
=======

The `conf` system supports setting actions. This allows for a flag to set an action
within the parser. All of the flags for action that are supported by Argparser are
supported here: https://docs.python.org/3/library/argparse.html#action

.. code-block:: python

    CONFIG = {
        'cheese': {
            'default': False,
            'action': 'store_true',
            'help': 'Say yes to cheese!',
            },
        }

Grouping CLI Options
====================

Sometimes it is helpful for multiple CLI arguments to appear as a group. Just
adding the `group` key is all you need:

.. code-block:: python

    CONFIG = {
        'cache_dir': {
            'options': ['-C', '--cacheland'],
            'group': 'global',
            'default': '/var/cache/',
            'help': 'The place to cache stuff!',
            },
        'config': {
            'default': '/etc/config.toml',
            'group': 'global',
            'help': 'The location of the config file',
            },
        'cheese': {
            'default': False,
            'action': 'store_true',
            'group': 'app',
            'help': 'Say yes to cheese!',
            },
        }

Using Config Files
==================

Enabling `conf` to read in config files can be done by just adding the options
to the config dict. Add `config` to your CONFIG dict and `conf`
will look for a config file at that location:

.. code-block:: python

    CONFIG = {
        'config': {
            'default': '/etc/config.toml',
            'help': 'The location of the config file',
            },
        'cache_dir': {
            'default': '/var/cache/',
            'help': 'The place to cache stuff!',
            },
        }

Now when you call `conf.reader.read` it will also look for a toml file in the
location that is defined for config. TOML is the default but you can specify
yaml or json, or you can use `config_dir` to scan an entire directory for
multiple config files.

Using Nargs
===========

Using `nargs` allows you to set up how many space delimited arguments are
accepted by the option. This value is sent down to the Argparser nargs
options. To see what can be passed in for nargs take a look at the python docs:
https://docs.python.org/3/library/argparse.html#nargs

Using Positional args
=====================

Often is makes sense to use positional arguments for your CLI options. This
can be easily added to `conf`:

.. code-block:: python

    CONFIG = {
        'name': {
            'positional': True,
            'nargs': 1,
            'display_priority': 1,
            'help': 'The name of the thing',
            },
        'stuff': {
            'positional': True,
            'nargs': '*',
            'display_priority': 2,
            'help': 'The stuff you need and want',
            },
        }

By using `positional` and `display_priority` you can determine the order of
positional arguments. Keep in mind that if you set nargs to '*' that will need
to be the last argument.

Rendering CLI Data
==================

Sometimes options on the command line need to represent complex data, such
as `dicts`. To accomplish this the `render` flag can be set. This allows
for a cli argument to be rendered through something like yaml or json:

.. code-block:: python

        'mapping': {
            'default': {'foo': 'bar', 'baz': 'quo'},
            'render': yaml,
            'help': 'A map of the things',
            },
        }

Now this command line will load into a dict:

.. code-block:: bash

    my_command --mapping 'cheese: yes, bread: no'

More importantly, this allows for complex default data to be made available
without sacrificing command line flexibility.

Enable OS Variables (Environment Vars and Registry)
===================================================

Enabling OS variables as configuration sources for a given value can be easily done.
An OS source is defined as an environment variable on Unix style systems and as an
entry in the registry on Windows

Just add the `os` option to the values passed to the key in the configuration dict:

.. code-block:: python

    CONFIG = {
        'output_color': {
            'default': 'red',
            'os': True,
            'help': 'The color to print out',
            },
        'test_extra_options': {
            'default': 'reactive',
            'os': 'TESTEXTRAOPTS',
            'help': 'Test mode for the extra options',
            },
        }

The `os` option can be set to `True`, in which case the variable that will be read
is the key. Or the `os` option can be set to a string which will
be used to read the option. In the case os unix style systems the environment variable
will be all uppercase to follow the standard convention.

Using Subcommands
=================

Subcommands allow for the cli application to accept a second command, like the
`git` command has `git clone` and `git commit`. To use subcommands just add
another dict to define the subcommnds:

.. code-block:: python


    SUB = {
        'sub': {
            'desc': 'a subparser!',
            'help': 'Some subparsing',
        },
    }

    CONFIG = {
        'foo': {
            'sub': 'sub',
            'help': 'Set some foo!',
            },
        }

So now you have a subcommand called `sub` and then under the subcommand the option `foo`
resides.
