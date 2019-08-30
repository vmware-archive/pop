.. _dyne_name:

=============
Dynamic Names
=============

The Dynamic Names system in `pop` is used to implement part of the app merging system.
When you think of app merging you should think of it as coming from 2 separate directions,
once direction is the ability to merge many apps together into a larger app. But the other
angle of app merging it to allow for external applications to extend your own subsystems.

Think of it this way, you define a system that detects information about a server, but
you don't want to have to build in support for all the specifics that could be discovered
on multiple operating systems and platforms. Instead of trying to maintain support for
20 operating systems in one application, you can instead make the core of the application
and then set up dynamic names, then you can have separate packages that gather data
for each specific platform but the separate packages dynamically add their own plugins
to your plugin subsystem.

This is what Dynamic Names allows you to do! Using Dynamic names is very easy, first
just define the `dyne_name` as the only option when you set up your new sub:

.. code-block:: python

    hub.pop.sub.add(dyne_name='grains')

Then in your project's *conf.py* file used by the conf.integrate system just add another
dict called `DYNE`:

.. code-block:: python

    DYNE = {
        'grains':[
            'grains',
                ]
        }

Inside your `DYNE` config you specify which `dyne_names` you want to add modules to and
what the module path, relative to your project is.

Now you can start up a new sub that will gather plugins from multiple systems that add
the dyne_name that you have set up!
