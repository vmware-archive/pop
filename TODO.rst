==========
Rosso TODO
==========

Distributed systems need to be able to distribute balanced software to execute
within worker pools and within the main management process arbitrarily across
many nodes auto located based on system properties and needs.

All functions of application execution need to be encapsulated within these
distributed software systems. From managment to serverless, from databases to
blockchains.

Applications expressed in packs
===============================

A distributed multi part application needs to exist that can use grains to map
usage to multiple nodes dynamically.

Subsystems need to be distributed and deployed automatically

Subsystem distribution
----------------------

Subs need to be able to have deps, init routines and a tarball based delivery
system.

Agents
------

There needs to be agents that can create interconnected links and be used as a
conduit for software distribution.

Software initialization
-----------------------

Software systems need to be able to be initialized either within the agent or
within a dedicated, or shared worker pool.