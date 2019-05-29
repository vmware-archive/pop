====
POP
====

Pop is used to express the Plugin Oriented Programming Paradigm. The Plugin
Oriented Programming Paradigm has been designed to make pluggable software
easy to write and easy to extend.

Most large projects eventually need to follow a modular and pluggable design,
so why not start a project using a plugin design?

Pop can be used to extend an existing project to add plugins, or to build
a project that is 100% pluggable.

Usage
=====

Using `pop` is amazingly easy, but deeply powerful. To start  an application
with `pop` just install pop and run the `pop-seed` script:

::

  pip install pop
  pop-seed poppy

Now a new python project has been created for you with a setup.py file,
execution script and your first plugin subsystem called `poppy`.

When you run your project it will set up `pop` for you and the application
starts with the `new` function inside newly created file `poppy/mods/poppy/init.py`.

Plugin Oriented Programming Manifesto
=====================================

Software development needs to evolve to work with larger software projects
and larger, more distributed teams.

Modern software development has been built on proven, powerful development
models. These models were introduced in the distant past and have been
deeply validated. These development models evolved from the models used
to create early computing systems and languages.

Plugin Oriented Programming takes an approach to programming that stems from
the developer first. Instead of making programming models that express how a computer
works, Plugin Oriented Programming takes the approach of making development
easier for developers and teams, both open and private.

Finally, Plugin Oriented Programming does not seek to supersede other
development paradigms, it is not a revolution, it is an evolution. Inside
POP you can use OOP, Functional, Procedural paradigms and more. Pop instead
gives a canvas to create pluggable interfaces that can be easily used to
expose functionality.

POP Concepts
------------

Plugin Oriented Programming is expressed through a number of concepts. These
concepts grow out of a decade of developing plugin based systems and plugin software.

These listed concepts are the high level concepts of Plugin Oriented Programming. Of
course there are a number of smaller concepts, but these define the high level view
of the paradigms.

The Hub
~~~~~~~

Pop creates a `hub` around which all assets, plugins, variables and communication occurs.
The `hub` allows for plugins to be shared between each other, so plugin systems can cross
communicate.

Plugin Subsystems
~~~~~~~~~~~~~~~~~

Plugin subsystems allow for new plugin containers to be defined. A plugin subsystem
is where the plugins reside and are available on the `hub`.

Patterns
~~~~~~~~

Plugin `patterns` are patterns used to define how a plugin system should behave.
Some plugin systems are library functions, some are used to generate data, some are used
to pipeline processing etc. Defining a plugin pattern allows for the creation of
code models so that plugins can fit inside of plugin subsystems easily.

Contracts
~~~~~~~~~

Contracts allow for plugins and plugin subsystems to be enforce. A contract is
used to enforce that new plugins follow the defined patterns for the given
plugin subsystem.

Shared Data
~~~~~~~~~~~

Shared data is critical for Plugin Oriented Programming. The `hub` combined
with plugin subsystems create a hierarchical namespace. This namespace, by
convention, defines if data is private, protected or shared. This allows for
smooth data hand offs between subsystems while still making data only
modifiable to certain areas of the code. The shared data concept is also
very useful when working with async code, as queues and events are available
to the application in a simple, shared way.

Application Merging
~~~~~~~~~~~~~~~~~~~

Merge able applications is the concept of multiple applications can occupy
the same hub, or be merged. This allows for better compartmentalization of
applications while still be able to combine many small applications into
a single large application.

POP Vision
----------

This expression of Plugin Oriented Programming works very well inside of
Python. Because of the flexibility of Python objects and namespaces it was
an optimal language to build `pop`.

But moving forward I would love to see Plugin Oriented Programming become
a reality in more languages. The paradigm allows for hot swappable plugins,
but this is not a requirement. I would love to see Plugin Oriented Programming
exist in a language like Go, where everything is compiled to a single binary.
I think that some languages have the optimal makeup for Plugin Oriented Programming,
particularly Julia, but also other dynamic languages.
