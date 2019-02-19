=====================
Configuration Reading
=====================

One of the classic issues with systems software development is adding
configuration and options to CLI programs. The problem is that configuration
data needs to come from multiple sources. Defaults need to be set, CLI options
need to be accepted, config file(s) needs to exist. Config file settings need to
override defaults, while CLI options need to override both, but the CLI needs
to be able to define the location of the config file(s). Finaly there ends up
being multiple sources of truth. Config options are documented in mone place
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

To use `conf` start by adding the `conf` subsystem to your hub (`conf` does not have an init):

.. code-block:: python

    hub.tools.sub.add('conf', pypath='pop.mods.conf')

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

Adding Extra CLI Options
========================

Grouping CLI Options
====================

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

Often is makes sense to use positional arguments for your cli options. This
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

Bys using `positional` and `display_priority` you can determine the order of
positional arguments. Keep in mind that if you set nargs to '*' that will need
to be the last argument.

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