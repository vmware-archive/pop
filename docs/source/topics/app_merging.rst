.. _app_merging:

============================
Application Merging Overview
============================

Application Merging is one of the most powerful components inside of Plugin
Oriented Programming. This is the idea that since an application is comprised
entirely of plugins using a predictable memory namespace, one should be able
to take full applications and merge them onto a single hub, and a single
application.

There are a number of goals and motivations for this concept. First off it
enforces good software development, forcing that rules are followed in
keeping the structure clean to avoid doing things that will violate app merging.

Some things that violate app merging are creating multiple hubs in an application
as the merged app can get confused on how to address namespaces.

.. note::

    The ability to make multiple hubs is deeply discouraged, but so is making
    singletons. The ability to have multiple hubs should always be supported
    to maintain a clean separation of the hub from the underlying programming
    language implementation.

Another violation of app merging is to not follow the hub namespace rules, this
creates opportunities for namespace collisions.

Why is App Merging a Big Deal?
==============================

The model inside of POP is not only built to make plugins easy to use, and make
some cool namespaces, but to enable app merging.

When looking at any idealized concept, social, political, theological, engineering,
etc. we paint a picture of an ideal world. We say that "Only if people would follow
this ideal, all would be well".

This is a grossly naive assertion to make on humanity, that we as humans seem to
never stop making. Even when a philosophy is presented to compensate for human
weakness we tend to corrupt that philosophy. So instead of looking at a concept
through the eyes of an idealized future we should look at concepts as ways to
compensate for human weakness while looking to accomplish real goals.

In application development we know that applications that are developed as collections
of libraries present more reusable components. But in reality this ideal not often
realized. This is because the creation of the application is the fundamental goal.
Writing software is not about elegant engineering as much as it is about producing
results. Any experienced software engineer has seen both sides of the spectrum,
projects that are garbage because business goals drive poor engineering and projects
that never see the light of day, or don't present a strong use case because so
much energy has been put into clean engineering that the project becomes pure art,
the only purpose it has is itself.

POP presents interfaces to users in an attempt to solve this problem. Allow developers
to natively and quickly create applications that solve busies needs but natively
present themselves as clean, re-usable, library driven applications that can be
easily re-used, in part or in whole.

The hub, plugins and patterns enable this! If an application is comprised of plugins
then interfaces that need extending or re-purposing can be easily added inside
a merged app. Patterns present isolated processes that deliver standalone value.
This allows us to extend many of the merits of OOP, now we have, not only data
and functions brought together, but we have entire application workflows
encapsulated in reusable patterns.

App Merging Collision Points
============================

When following POP there should be few app merging collision points. If namespaces
are kept clean, and if namespace rules are followed, then the result is one where
collisions should rarely occur.

The place where collisions are very like to occur though, is in configuration
merging. This presents a truly serious issue. The conf system is built to resolve
the collision problem to the smallest possible surface area. That surface area is
the input level, where the configuration data is presented from the user.

Once the configuration information is loaded into the hub it has been namespaced
and made available on the respective namespace used by the subs. But before that
it needs to be read in from the cli. This is what the `conf.integrate` system
is designed to solve. The information read from the conf.py files can be modified
to resolve collisions without having an effect on the operation of the underlying
configured systems.

How do I App Merge?
===================

Acctually doing an app merge is simple, it is really done in 2 places.

First, when you call `conf.integrate` the first option is a list of the apps you
want to load configuration from. Just add the top level python import you want to
use to the list of `conf.integrate` interfaces.

Second, add the subs to your hub, you will likely need to start up the subs and make
your high level app start using the interfaces exposed by the subs, but that
should be it! You should be able to add subs onto your hub just like they are really
powerful classes.
