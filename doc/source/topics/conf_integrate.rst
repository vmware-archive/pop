====================
The Integrate System
====================

Now that you have a clear view of the available constructs in configuration dicts used by
the `conf` system we can talk about the `conf.integrate` module. By itself `conf` is a great
tool to load configs, but `pop` is all about dynamically merging multiple plugin subsystems.
Dynamically merging applications presents a significant issue when it comes to configuration,
`conf` and the `conf.integrate` systems are designed to work together to solve this issue.

Using `conf.integrate` is made to be as easy as possible, but it also means that the
configuration system follows a clear model.

When making a `pop` project, everything is a plugin, but you may have noticed that the
`pop_seed` script makes two python files outside of the plugin system. These files are
`version.py` and `config.py`. The `version.py` file is hopefully self explanitory. But
the `config.py` file needs a little explanation.

The Three Config Dicts
======================

The integrate system uses this config.py file to simply define CLI options, local config
options, and options that we assume other systems would share. These three types of
configuration data are defined in three configuration dicts in `config.py`.

Simple populate these three dicts with configuration data and it can be easily
and dynamically loaded by other `pop` projects.

CONFIG
------

The `CONFIG` dict is where the configuration options used specifically by the subsystems
defined in this project.

CLI_CONFIG
----------

The `CLI_CONFIG` dict is used for configuration data data specific to the command line.
It is typical to set positional arguments here, things that define the structure of how
the CLI should be processed.