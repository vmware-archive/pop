==========
Quickstart
==========

Using pop to create a plugin oriented project is easy. Pop comes with a simple script to build
the basic parts of a pop project. The `pop_seed` script builds the directory structure and
adds a setup.py that autodetects all new plugins and a script for your new project.

Just pick a directory to start in and run pop_seed:

.. code-block:: bash

    pop_seed poppy

This command will make a new project called poppy, the setup.py, requirements.txt, a
script to run the project and the directories to hold your first plugin subsystem.

With these assets at hand you can run the application however you please, via system
installation, pyvenv, docker etc.

In the scripts directory you will find a script called `poppy`. If you open it up you
will see the simple creation of a pop project. The creation of the hub, and the setup of
the first plugin subsystem. As well as the call to run the first code.

The first code to run is in the file `poppy/mods/poppy/init.py`. There you will find
the `new` function. The `new` function is used to initialize a plugin subsystem when needed.

Next open up the poppy subsystem's `init.py` file:

`poppy/mods/poppy/init.py`:


.. code-block:: python

    def new(hub):
        print('poppy works')


With a project up and running you can now add more plugins, more code and more subsystems!

Next take a look at how to call functions within a pop application, then the pop conventions
and how to think in pop.
