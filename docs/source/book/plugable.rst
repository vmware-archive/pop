==================
Define "Pluggable"
==================

This section deinfes what makes code plugable, some of the concepts here will
be new to you, that is OK. A programming paradigm cannot be created without
exposing a number of concepts and terms. Many of these terms are explained
in much greater depth later in the text. Knowing the basics around the 
rules of pluggablity and how the macro concepts fit will aid learning them
in greater depth later on.

Come back to this section over and over again, these rules should help you to
structure in your mind how to make truly pluggable software.

For Plugin Oriented Programming, virtually everything becomes pluggable. But what
does it mean to write completely pluggable code? How can a paradigm allow you to
author completely modular code? What is pluggable into what, and how?

To answer this, it is necessary to explain a number of the concepts of Plugin
Oriented Programming. These concepts will give an introductory foundation for
what Plugin Oriented programming is and how to train yourself to think in a
world of plugins.

These concepts will also define how to avoid breaking pluggablity. Each layer
should be worked with in a pluggable way as to avoid breaking the concepts of
Plugin Oriented Programming. If these concepts are not broken then the application
should achieve the goals of being truly pluggable.

Collections of Plugins - Subsystems
===================================

The first aspect of Plugin Oriented Programming is to consider all code as being
broken up into individual plugins. Each plugin adheres to an interface definition.
This concept of an interface definition makes each plugin, pluggable. This means that
the interface definition becomes a critical component of your application and
application thinking. The interface defined by a single plugin, through its very
existence, defines part of the structure of your application.

Each plugin is replicable and extensible. If ever a plugin becomes too large, or
too unwieldy, then it needs to be broken up.

Plugins all belong to plugin subsystems, or *Subs*. The plugins present interfaces
to communicate with the plugins, but *Subs* also present interfaces. We call these
interfaces *patterns*.

Rule 1 of Pluggability
----------------------

*Subs* contain *Plugins*, plugins express an interface the is compatible with the
pattern defined by the *Sub*. If plugins exist inside of a *Sub* that do not adhere to
the interface of the sub, then they should be placed in another *Sub*. This other
*Sub* can be new, or an existing *Sub*.

Rule 2 of Pluggability
----------------------

Plugins must be small, interfaces must be simple. If the code in a plugin cannot be reasonably
explained to another engineer in a few hours - to the extent that the new engineer can extend
or maintain that plugin - then it is in violation of pluggability.

The same applies to *Subs*, if the interface presented by a *Sub* cannot be reasonably explained
to another engineer in a few hours - to the extent that the new engineer can extend
or maintain that *Sub* - then it is in violation of pluggability.

The Hub and the Namespace
=========================

Plugin Oriented Programming functions based on the idea that a strict hierarchical namespace
is maintained. This namespace defines where *Subs* and plugins live, as well as data.
The *Hub* is the root of the namespace, and each *Sub* is available on the *Hub* or below
another *Sub*. Each plugin lives in a *Sub*. Data is stored on the *Hub* so that it can be
made available to the rest of the application and can be properly tracked.

Variables stored on the *Hub* should be stored nest to the systems that have write access to
them. If all plugins in a *Sub* have write access to a variable, then it is stored under the
*Sub*'s namespace on the *Hub*. If multiple *Subs* need write access to a variable, then those
*Subs* must be stored within a higher level *Sub* which contains that variable.

Finally, the namespace data, subs, plugins and data should follow naming conventions to
ensure consistency. Variables on the hub should always be all caps. Functions, *Subs* and
plugins should always be underscore delimited, all lower case. Class names should always
be CamelCase. These simple rules ensure that namespace collision probability is low,
and presents predictable information to the next engineer.

Rule 1 of Namespace
-------------------

Variables are stored on the *Hub* relative to the *Subs* and plugins that have write access
to the data. Any plugin or *Sub* deeper on the *Hub* than the variable have write access to
the variable. If a plugin that is not below a variable wants write access, that variable needs
to first be copied within that plugin's respective namespace.

Rule 2 of Namespace
-------------------

Conventions must be followed to ensure consistency and ease of transfer. Variables on the *Hub*
should always be all caps. Functions, *Subs* and plugins should always be underscore delimited,
all lower case. Class names should always be CamelCase.

App Merging
===========

App Merging defines how multiple applications can be merged together. Since Plugin Oriented
Programming applications all have a predictable namespace, those namespaces can be merged
from multiple apps.

This makes entire applications natively pluggable! So long as a few simple rules of App Merging
are not violated.

Everything goes on the *Hub* if code is intended to be a library then it should be treated
as such and developed as a standalone codebase that exposes library functionality. All
code in a Plugin Oriented Programming codebases must exist in the structure of the *Hub*.

Plugins and *Subs* have initializers, much like classes in Python. These initializer
functions are called `__init__` and they are called when the plugin is first loaded. This
allows for any environmental aspect required by the plugin or *Sub* to be set up. This is
typically adding data structures to the *Hub* that are needed by the plugin or *Sub*.
The initializers should never begin the execution of the code in the plugin or *Sub*.
If they do initialize the code within the plugin or *Sub* then this can break App Merging
because when the Sub is merged into another application it begins functioning. Those
functions and patterns should only be executed at the behest of the merging application.

App Merging exists to allow for applications to be split into small, workable, codebases.
Then the many codebases can be merged together using a lightweight codebase to bring
it all together. Just as *Subs* and plugins should be transferable to a new engineer
within hours, so must an app. Apps should be small enough that they can be explained
to a new engineer - to the extent that the new engineer can extend or maintain that *Sub* -
within one to few days. If this cannot be done, then a new app should be created to
partition out and isolate the next chunk of code.

Rule 1 of App Merging
---------------------

Everything on the *Hub*. Writing library code outside of the *Hub* should be relegated to
a separate codebase.

Rule 2 of App Merging
---------------------

Don't execute sequencing code inside of initializers, only set up the environment.

Rule 3 of App Merging
---------------------

Apps should be small enough that they can be explained to a new engineer - to the extent
that the new engineer can extend or maintain that *App* - within one to few days. If
this cannot be done, then a new app should be created to partition out and isolate the
next chunk of code.

