.. _story_of_pop:

==============
Origins of POP
==============

I (Thomas Hatch) am the creator of a major systems management platform called Salt and
the founder and CTO of SaltStack. As I developed Salt I found that a plugin approach
suited our needs so well that I became increasingly enamored with plugins.

Salt was originally developed with and for plugins, but only in isolated areas. But
over time I added more and more plugin subsystems. As things moved forward I discovered
that major components of Salt we being defined entirely within plugin systems. It
also became a major desire to make more systems within Salt pluggable. We found that
this made Salt more approachable by developers and amazingly extensible. But we also
found a number of shortcomings in the design. When we have plugin systems we wanted
to reach out to those plugins more and more from other parts of the code. We also
found that we were dealing with such vast quantities of plugins that maintainability
became an issue.

In response to this I started to develop the POP concept. I did not have a lot of spare
time, so it took me a few years, but I was able to find elegant solutions to many
of these problems. Over time I became tied to the idea of POP. Over and over again I found
myself rapidly developing software platforms using POP as an amazing shortcut.

Subsequently I was able to find shortcomings in my designs and I repeatedly rewrote
the POP platform. The platform you now see is actually the fifth iteration and something
that I feel is finally ready to be shared with the world.

I hope that this iteration will allow people to make the most of the POP paradigm and
to be able to help fill out how to use POP to solve more software engineering problems
that we face today.

Software today has evolved into an incredibly distributed affair, with global teams
often from many companies with innumerable goals and objectives. The POP system is
an attempt to find a better way to help these teams collaborate and interface while
still enabling large scale development.
