.. _hub_overview::

=====================
Understanding The Hub
=====================

The hub is the central feature of Plugin Oriented Programming. I first developed the idea
of the hub when I implemented pop in Julia. I realized that I needed to pass in a namespace
for all of the plugins to exist on. Before that I had been trying to maintain links between
plugin systems on the python module level. Working in Julia forced me to think about the
problem differently. The hub therefore allows for plugin systems to be seperated from the
module systems inside of (in this case) Python.

Once I had a seperate namespace to work with it became easy to decouple memory management
as well. I had created a data higherarchy.

This is a very critical part of POP, memory and variable management is very important to
how software it written and I realized that a new exploration of how to approach the
problem could yield new results.

Namespaces Beyond Silos
=======================

The first thing to think about the hub is that is defines the complete structure of your
application while delivering a new way to think about memory management. Namespaces, beyond
silos.

In classical Object Oriented Programming we follow a model of variable namespaces where
we isolate memory onto the stack and the heap. The clean, well defined stack of a function,
and the broad mess of data, aptly called the heap. To deal with the open ended flexibility
of the heap memory management evolved into an ajacency model. Data that is to be used by
certian functions should be ajacent to said functions inside of class instances. This made
memory management on the heap (arguably) more elegant. You don't need to manage a heap
of variables, but instead a collection of class instances. This has generally been seen as
an improvement, an evolutions.

But this created a reverse issue, data incresingly became isolated to silos, encapsulation
offered control, but introduced over encapsulation. The idea that data became too isolated
and hard to get access to. It is a common issue that data needs to be synced between classes
and instances and that communication between classes and instances can be troublesome. There
now exist many ways to solve this problem, but they often remain messy and convoluted.

Object Oriented Programming also introduced the concept od public, protected and private
variables and functions. This is an excellent tool for defining how the developer wants
to scope the use of functions, variables and methods.

POP pushes beyond OOP without sacraficing the benefits. The hub presents a namespace that
can be used to place data onto a world readbale medium, solving over encapsulation, while
still communicating to the developer how to interact with data and still allowing data
to be private to functions, modules, classes, and instances.

Using Hub Namespaces
====================

The hub namespace is made to link to the physical layout of the code. Therefore the location
of data on the hub also defines the location in code where the data is to be used and how.
Lets start by going over the hub's layout.

hub
---

The hub is the root object, if you decide to place variables on the hub, it is assumed that
these variables are world read/writable. It is rarely, if ever, permissible to place variables
directly on the hub. This is because it dirties the root namespace and creates issues
for app merging because you have a higher likelyhood of creating app merging conflicts.

hub.sub{.sub.sub...}
--------------------

Below the hub is where you get your subs. The subs are really the sole intended ocupants of
the hub. A sub is a named collection of plugins. In this case, variables that exist on the
sub are intended to be writable only to plugins found within the sub.

A sub can also have a nested sub, this is a sub within the sub that has its own plugins.
A nested sub is intended to have write access to the parent sub's variables. This
allows for communication dicts, queues etc to exist on a higher level sub the facilitate
communication between lower level sub's modules.

The sub level is a very common level to place variables. The nature of plugins is such that
they need intercommunication. But that communication does need to be limited! It should
not experience interference from external plugin systems.

Keep in mind that this is the data from external plugin systems. Many patterns are build
to present external communication interfaces to other subs. This is a perfectly acceptable
reason to have external subs send data into a sub. But this is typically done by calling
a function within the sub, so the data is still written from within the sub itself. This
allows for the data input to be controlled and kept clean.

hub.sub.mod
-----------

The module layer allows for data that is isolated to the use of the specific module. This
allows for patterns that calls functions in modules repeatedly to persist data.

Naming Conventions
==================

Because the namespaces can collide it makes sese that objects on the hub should follow
namespace rules, use this document to define access and naming conventions.

Variable Names
--------------

Variable names stored on the hub in any location should always be all caps, following the
Python convention of module level variables:

    hub.sub.INQUE = asyncio.Queue()

Sub Names
---------

The names of subs should always be underscore delimited and lower case:

    hub.sub

Module Names
------------

The names of modules should always be underscore delimited and lower case:

    hub.sub

Function Names
--------------

The names of functions should always be underscore delimited and lower case:

    hub.sub.mod.function()

Class Names
-----------

Class anmes should always be CamelCase:

    hub.sub.mod.MyClass()
