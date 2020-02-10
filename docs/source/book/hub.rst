=======
The Hub
=======

Plugin Oriented Programming is all about namespaces. Plugin interfaces are
dynamic, otherwise they would not be plugins, therefore if they need to be
stared with each other, they need to have a communication medium. Instead
of making a complicated API interface for the plugins to communicate `pop`
allows all of the plugins on the system to be accessed via a shared
hierarchical namespace.

All of the plugins in the application can be reached by traversing the
namespace that is the `hub`. Plugin subsystems can exist on the hub and
plugin subsystems can contain more plugins subsystems and plugins.

But the `hub` is not just for plugins, we need to be able to store data
associated with our functions. The data is stored on the `hub`, in locations
in the namespace relative to where the functions that use that data reside.

Getting Stated With the Hub
===========================

The `hub` is the root of a `pop` project. Before we can start working with
`pop` we must first create the `hub`. Normally, when using `pop-seed` you don't
even need to consider where the `hub` comes from, as `pop-seed` creates the
`hub` for you in the startup scripts. But this document is intended for
understanding, so lets look at a `pop` app from the ground up.

.. code-block:: python

    import pop.hub

    hub = pop.hub.Hub()

Well, that was easy! Now we have a `hub`! When working on an existing codebase
it is easy to wonder "Where did this hub come from?". The `hub` is created in
the `run.py` file, and the first function is called from there as well.

Once the hub is created, and the first function called, then the `hub` is passed
to each function as the first argument. This is just like classes in python where
each function receives the self variable as the first argument.

The First Subsystem - pop
=========================

When the `hub` is created it comes pre-loaded with the first plugin subsystem. A
plugin subsystem is often referred to as just a `sub`. This first plugin subsystem
is called `pop`. It contains the tools needed to extend the `hub` and add additional
`subs`.

When calling a reference on the `hub` the full path to the reference is called. This
allows for all code to always exist in a finite, traceable location.

.. code-block:: python 

    import pop.hub

    hub = pop.hub.Hub()
    hub.pop.sub.add('poppy.poppy')
    hub.poppy.init.run()

The `pop` `sub` contains a plugin called `sub` which is used for managing `subs`.
Inside we find a simple function called `add`. This function allows for adding
new plugin subsystems onto the `hub`.

The `hub.pop.sub.add` function is very robust, allowing for new plugin subsystems
to be added to the hub in many ways. The most common way is to use *Dynamic Names*
which allows for *Vertical App Merging*. This is covered in much more depth in the
section on *Subs*.

Once the new `sub` has been added to the `hub` it can be referenced. The `hub` is
not a complicated object, like everything in `pop` it is designed to be easily
understood and simple.

Now that you have a basic understanding of the `hub` we can move on to *Subs*.
After you have a good understanding of *Subs* We can come back to the `hub` and
go into more depth on how these critical components work together.
