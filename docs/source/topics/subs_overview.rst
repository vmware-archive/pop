.. _subs_overview:

==========================
Plugin Subsystems Overview
==========================

Plugin subsystems, or `subs` are the main container type used inside of `pop`.
These `subs` contains the collections of plugins, patterns, contracts, and interfaces
that drive your application. Fortunately adding `subs` to your `hub` is easy to do and
adding plugins to your `subs` is equally easy. All of the namespaces, tricky plugin
loading and tracking are all taken care of in `pop`.

When you add a `sub` you have many options. Most of the demo subs you see will be
very simple, just a call to `hub.pop.sub.add` with only the pypath variable
specified. This is all you need in most cases! But you can do much more powerful things
when loading up a new `sub`!

The init.__init__ Function
==========================

The first thing to be aware of in `pop` is the `init.__init__` function. When you make a new `sub`
the *init.py* file is treated as the initializer, or pattern definer of the `sub`. This file
does not need to exist to have a sub, but it exposes extra functionality. The main thing to be
aware of is that if the `__init__` function is defined inside the *init.py* file then it will
be executed when the subsystem is loaded. The first argument passed to the `__init__` function
is, as usual, the hub, and the sub object that the *init.py* has been loaded onto is available.
This makes it easy to initialize any data structures that might be needed on the `sub`.

Directories and How to Find Them
================================

Plugin loading is all based on the directories that contain the *.py* files that constitute
plugins. When the `pypath` argument is passed in python imports that path, then it derives
what directory that path is and adds it to the directories to be scanned. The directories
used by the `sub` can be loaded via a number of options:

    pypath: A string or list of python imports that import a python package containing plugins

    static: A string or list of strings that are directory paths containing plugins.

    contracts_pypath: A string or list of strings that import a python package containing plugins to load contracts

    contracts_static: A string or list of things that are directory paths containing plugins to load contracts

Dynamic Name
============

The Dynamic Name function is amazingly powerful. It allows you to specify a dynamic loader name
that pop will detect in your Python path and auto load extra plugins from external Python
packages that have defined them. This is an amazing way to dynamically make your plugin
subsystem even more pluggable by allowing external applications to extend your system.

The Dynamic Name system is used by adding the option `dyne_name`. It is the only required
optiuon when enabling dynamic name, But it also requires that your application adds the
`DYNE` flag to the conf.py file in the root of your project.

    dyne_name: A string which defined the name of the subsystem, and how to map it using the
    Dynamic Name system

For more information on Dynamic Names please see the doc outlining how the Dynamic Names system
works and how to use it: :ref:`dyne_name`

Omitting Components From the Sub
================================

When modules are loaded, they by default omit objects that start with an underscore. This is set
to allow for objects to be kept private to the module and not expose them. The character used
to determine if the object should be omitted can be changed, or it can be set as an endwith char:

    omit_start: The char to look for at the start of all objects to determine if it should be omited, defaults to '_'

    omit_end: The char to look for at the end of all objects to determine if it should be omited, disabled by default

    omit_func: Set to True to omit all functions in the sub

    omit_class: Set to True to omit all classes in the sub

    omit_vars: Set to True to omit all vars from a sub

If you choose to change any of these values in your default settings for your `sub` it should be heavily
documented, as it will really confuse users of your sub and it is strongly discouraged!!

Stopping on Load Failures
=========================

It can be good to set the sub loading to traceback if a plugin fails to load. Because plugin
interfaces allow end users to add plugins and potentially dirty up the code, by default
if a plugin fails to load it does not stop the sub from loading.
If you do want the sub to traceback set:

    stop_on_failures: Set to True to make the sub traceback on failures to load plugins propogate up

Virtual Execution
=================

When modules are loaded they execute the `__virtual__` function. The `__virtual__` function
can be disabled for a sub when it is loaded. This is typically used just for debugging.

Modify the Initializer
======================

By default the `__init__` function is run when the sub loads. This can be disabled by setting
the `init` value to False:

    init: Set to False to disable running the `__init__` functions for all modues

Multiple Python Module Objects
==============================

When plugins are loaded they are imported into the python module tracking system in a specific
module path. If you want to be able to load the plugins multiple times and have them exist
in multiple namespaces then you can via `mod_basename`. You only need to do this if you are
loading persisted data onto the module level. If you are doing this then move your data
onto the `hub`:

    mod_basename: Pass a string to specify the Python sys.modules namespace to load the module onto
