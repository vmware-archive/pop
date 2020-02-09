=============
Origin of POP
=============

If Plugin Oriented Programming claims to address difficult problems in modern software
engineering, then it needs to have come from earlier attempts to solve these problems.
Plugin Oriented Programming originates from development models that have been well
established and is derived from successful software.

Plugin oriented design aspects have long driven large scale development, most
large software projects incorporate plugins and modular design. But plugins are almost
always an afterthought, pushed into the codebase after the fact and end up exposing
only a few plugin interfaces.

Salt's Plugin System and POP
============================

The creator of Plugin Oriented Programming, Thomas Hatch, is also the creator of one of
the world's largest open source projects "Salt". The design of Salt incorporated plugins
very early in the project and build a reusable plugin system.

The pluggable nature of Salt quickly became one of the main driving factors for the
project, making contributions easy and the platform flexible. Salt's plugin system, called
the "Salt Loader" was used to create many more plugin subsystems for Salt over the years
and is now used for over 35 plugin systems in Salt.

Adventures in Plugins
=====================

Thomas realized the benefits of plugins as they existed in Salt and began to explore how
to make a standalone plugin system. He made a plugin system which he called called "Pack",
but felt that it still had many of the limitations that existed in the Salt Loader. So
Thomas decided to attempt to make this plugin system in other languages. He made it in
Go, Julia, Nim, and a few others, but came out of the experience with new ideas about how
to approach the problem.

Thomas then wrote Pack2, but this version of the plugin system had many new components.
Pack2 was used by SaltStack to write a few software components and was eventually
deeply tied to a number of software projects within SaltStack.

But this experience also added to a deeper understanding about how plugin design should
work. Thomas at this point realized that he had not just made a plugin library, but that
he had create a programming paradigm. With this realization, Thomas renamed Pack to Pop
to reflect that the implementation had grown into Plugin Oriented Programming.

At this point Thomas changed how the plugin system worked, yet again, but his time his
view of the problem set had grown a great deal. Now he was able to overcome many restrictions
in the design and introduced the concepts around app merging and configuration merging.

At this point Thomas had created Plugin Oriented Programming. The journey through writing
mountains of code for many projects had led him to a much deeper understanding of programming
problems and new ways to solve them.

Emergence of POP
================

Plugin Oriented Programming was first released in late 2019 and began to gain a following. This
book was written in response to more and more people showing interest in Plugin Oriented Programming
and as the primary reference for the core concepts that make up Plugin Oriented Programming.
