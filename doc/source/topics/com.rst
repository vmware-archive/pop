========================
Com Communication System
========================

Pop comes fully loaded with a built in network communication system.
This system is contained in the sub `com`. `com` allows you to create
async connections to pools of local and remote systems. These pools than
allow for communication among these systems to be broadcast in a number
of different ways over asynchronous but fully tracked connections.

The communication pipes that are used are all based on websockets
so they are fast, reliable and based on well proven and vetted technology.

Using the com system might take a little gettign used to, instead of the
system being intended for simple point to point connections it is built
to handle a myriad of topological use cases, from point to point to
pub/sub and load balanced scenarios.

Pools, Routers and Connections
==============================

Instead of exposing network sockets and contructs, `com` exposes Pools
Routers and Connections. A pool is a collection of connections that all
use the same router. A pool can be a collection of both outbound and
inbound connections. This allows you to make natively bi-directional
interfaces which can operate over diverse network topologies.

A router is the function that handles the incoming message. The router
is a python coroutine. It can then process the incoming message with
full awarenes of the conection that sent the message.

Using com
=========

Using com is simple, although it may take a little getting used to.
Start by adding the `com` sub to your hub:

.. code-block:: python

    hub.tools.sub.add('com', pypath='pop.mods.com', init=True)

Once the subsystem is added to the hub then you are ready to go create
our first router. Since the router is the interface into the business end
of your application it is a critical component.

We will start by making a simple echo router, all it needs to do it accept
the correct arguments and return a simple serializable message.

.. code-block:: python

    async def echo_router(hub, ctx, msg):
        return msg

Thats it! Teh router is just a referenceable function on the hub.

Now that we have a router we can create a named connection pool.

.. code-block:: python

    hub.com.pool.create('worker', hub.my_sub.routers.echo_router)

Now the pool has been created and all data will flow through the router
for all of the connections made to this pool, so lets add some
connections.

Lets start with a 'bind' connection. This is what is typically called
a server, binding to a local port to accept outside connections.
One of the great things about `com` is that we can have
servers and clients in the same pool. This is where the bi-directional
topologies come into play making it easy to traverse multiple network
directions with your application.

.. code-block:: python

    await hub.com.pool.add_con('worker', 'bind', '127.0.0.1', 64444)

In this case we made a connection in the pool `worker` that we made
earlier, the type of connection is a 'bind'
(meaning a server style connection), to localhost port 64444.

Now lets make a client pool and some client connections to our new server.

.. code-block:: python

    hub.com.pool.create('req', hub.my_app.routers.echo_router)
    await hub.com.pool.add_con('req', 'client', '127.0.0.1', 64444)

Now we have an active bi-directional relationship! We can send from either
side and everything is seemless, `com` does not act like a server/client
relationship, but rather more like an open phone line, we can now just
talk.

We can send a message to a random member of the pool:

.. code-block:: python

    msg = 'No one expects the Spanish Inquisition!'
    ret1 = await hub.com.pool.rand('worker', msg)
    ret2 = await hub.com.pool.rand('req', msg)

We can talk to our connection pool in a number of ways. We can
publish to all connections using the pub async generator:

.. code-block:: python

    async for ret in hub.com.pool.pub('worker', msg):
        print(ret)
    async for ret in await hub.com.pool.pub('req', msg):
        print(ret)

As you can see, it does not matter which side we send from, the behavior
is the same.

Keep in mind that you can also add client and bind connections to the
same pool! So you can have a service that accepts connections
from one network and then reaches out to connections on another
network! Also since the underlying protocol is just an abstracted
away http websocket, we can use existing http technology
like load balancers and proxies.