=========
Contracts
=========

One of the core components of `POP` is the contract system. When everything
is a plugin then these plugins need to be able to enforce the interface
they belong to. `POP` provides contracts to enable these interfaces.
Contracts can be used to define plugin interfaces, ensure that functions
that are needed are available, and that needed functions follow argument
signatures. Contracts can also define transparent wrappers, running
pre or post functions around function calls, or replacing the actual
function call.

Signature System
================

The signature system allows for function signatures to be enforced in plugins
via contracts. This means that a plugin the implements a contract will be
forced to implement the named functions and follow the restrictions inside
defined by the function signature.

In a nutshell the signature system allows for contracts to define the
implementation interface for plugins.

If this file is defined as the contract `contracts/red.py`

.. code-block:: python

    def sig_foo(hub, a, b: str):
        pass

Then the file `red.py` is forced to create a function with a compatible signature

.. code-block:: python

    def foo(hub, a, b:str):
        return a + b

The signature system also verifies `*args` and `**kwargs` conditions, parameter
names, types and annotations.

So this `sig` contract:

.. code-block:: python

    def sig_foo(hub, a, b, **args):
        pass

Will work with this function:

.. code-block:: python

    def foo(hub, a, b, c, d):
        return a + b + c + d

Because the contract allows arbitrary `*args`, but in this example the contract
will mandate that `a` and `b` are defined.

Similarly `**kwargs` will pass through:

.. code-block:: python

    def sig_foo(hub, a, b, c=4, **kwargs):
        pass

Which allows a function like this:

.. code-block:: python

    def foo(hub, a, b, c, d=5, e='foo'):
        return a

Since the `sig` function in the contract allows `**kwargs`, the function can
have `**kwargs`.

Similarly, if the `sig` function does not have `**kwargs` then additional
parameters are NOT allowed beyond what is defined in the `sig`.

Wrappers
========

Contracts allow for functions to be wrapped. This allows for external
validators to be enforced, for parameters to be validated, and data to
me manipulated.

The available wrappers are `pre`, `post`, and `call`. When these are included
in a contract they will be called when the function is called.

Module and Function Wrappers
----------------------------

When creating wrappers, they can be applied to all functions in a module
or they can be applied to specific functions. To make a module level
wrapper, just make a single function with the wrapper type name:

.. code-block:: python

    def pre(hub, ctx):
        pass

This function will now be executed for every function called in the
corresponding plugin.

A wrapper can also be made to be specific to a function by using the
same function name, just prepend the function name with the name of the
wrapper to use, as in `pre_`:

.. code-block:: python

    def pre_foo(hub, ctx):
        pass

Pre
----

When using `pre` the contract function will be executed before the module
function. The `pre` function receives the hub and a `ctx` object. The `ctx`
object is used to contain the context of the call. This `ctx` object has
access to `args` and `kwargs` for the function call:

.. code-block:: python

    def pre(hub, ctx):
        if len(ctx.args) > 1:
            raise ValueError('No can haz args!')
        if ctx.kwargs:
            raise ValueError('No can haz kwargs!')

Call
----

The `call` wrapper can be used to replace the actual execution of the
function. When call is used the underlying function is not called, it
needs to be called inside of the call function. This function can be useful
when you want to have conditions around weather to call a function, or to
have a full context around the wrapping of the function. The function object
is included in the `ctx`:

.. code-block:: python

    def call(hub, ctx):
        return ctx.func(*ctx.args, **ctx.kwargs)

Post
----

The `post` wrapper allows for the return data from the function to be handled.
This can be useful if your function(s) need to modify or validate return data.
The return data from the `post` function is the return data send back when the
function is called.

.. code-block:: python

    def post(hub, ctx):
        ret = ctx.ret
        if isinstance(ret, list):
            ret.append('post called')
        elif isinstance(ret, dict):
            ret['post'] = 'called'
        return ret

Using the contracts Directory
=============================

Contracts can be added to a `sub` by just adding a subdirectory called `contracts`
into the directory containing the `sub` plugins. So if you have a sub called
`rpc` then the contracts directory would be `rpc/contracts`.

Inside the `contracts` directory the name of the modules will map to the name of
the plugin in the corresponding `sub`. The `virtualname` of the contract module is
also honored and will override the file name in the same way that `virtualname`
will override the file name in standard plugin modules.

This means that if you want a contract for a module called `red` then the file:
`contracts/red.py` will apply for the module `red.py`. Similarly if you want a single
contract to be applied to multiple plugins the implement the `red` interface just call
the contract module `red` and then have the modules that implement the interface take
the `red` `virtualname`.

Using __contracts__
===================

A plugin can also volunteer itself to take on a specific contract or a list of
contracts. This can be done with the `__contracts__` value at the top of a plugin
module.

.. code-block:: python

    __contracts__ = ['red', 'blue', 'green']

All of the contract wrappers and sigs will be enforced and called. If multiple wrappers
are defined for a given function then they will be called in the order in which they
are defined in the `__contracts__` variable.
