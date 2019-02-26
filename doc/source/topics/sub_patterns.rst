==================
Subsystem Patterns
==================

When making subsystems the best thing to do is make sure that the subsystem follows a pattern.
Patterns are the model for how a subsystem is used. When a pattern is used then all of the plugins
in the subsystem do similar tasks and follow similar models. Some patterns are good at specific
tasks, such as an rpc/rest backend. Some patterns are good at disparate tasks, like setting up
and running a server.

This document covers a number of common patterns, but you can create new patterns! Just make
sure that your pattern is well documented and contracted.

Spine Pattern
=============

The spine pattern is very common, because it defines the startup spine of an application. This
is a pattern where your application loads up config data, starts worker processes and loads the
bulk of the subsystems to be used.

The spine is typically the first subsystem loaded from the startup script. The spine should
be very small and only have a few plugins. Try to keep the spine very limited, and just
enough to start the application. The spine typically runs the following things:

* Set up the core data structures used by the application
* Load up `conf` and read in the application configuration
* Load up additional subsystems
* Start up an asyncio loop
* Start the main coroutines or functions

Beacon Pattern
==============

The beacon pattern is used to start up and maintain many coroutines. The beacon pattern adds
coroutines to a larger coroutine pool based on the plugins that expose coroutines. This
pattern is useful for downloading data from multiple sources, continually gathering monitoring
data, gathering system data on a regular interval, setting up multiple async watchers.
