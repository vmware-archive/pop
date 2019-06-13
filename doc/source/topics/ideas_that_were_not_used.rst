========================
Ideas that Were Not Used
========================

This doc is intended to track ideas that we thought were good at first but later
decided against. This way we can remember why we are not doing specific things and
track the the circumstances were at the time.

Modification of the Imported Module
===================================

When a module is imported Python loades the module object onto `sys.modules`. The
object on the `hub` is not the module but an object filled with refs to classes
functions etc. Early on we decided to make it easy to call functions inside the same
module by taking the wrapped function and then overriding the function on the
module object loaded into sys.modules.
We ran into some issues, like the module being imported outside of `pop` and
then getting changed by pop later on. We felt that it would be better to keep
the modules clean. This allows us to have multiple hubs and is less suprising to
users. The downside is that if you call a fuinction locally in a module then
it is not contracted and the hub needs to be passed in manually.