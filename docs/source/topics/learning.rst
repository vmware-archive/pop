.. _learning_POP:

============
Learning POP
============

Learning POP means thinking about programming differently, like any
programming paradigm. Start by letting go of how you think about programming.

Rule 1 - Memory Management
==========================

Classes are useful, but they are not the end all model for programming. Instead
of thinking about classes as the ultimate container of code and data think about
them as an interface to make types. This is the origin of classes and they are
very good about it. The problem with Classes has to do with data access
and over-encapsulation. When data is tied to a class it becomes isolated, and
so does the functionality. Instances are like little data prisons. Data should
be available to the entire program.

Woah you will say! Globals are bad!

You are right! Arbitrary globals are bad! But namespaces are not. The first
thing to accept with POP is the global namespace, the `Hub`. The Hub is the
shared root object in POP. Everything that you think of as being on the
heap, now goes on the Hub. The problem with the heap is that stuff gets lost.
This is where memory leaks come from. Instead of putting data on the heap,
put the data on the Hub. That way you can locate and track all of your data.

Coming to grips with the Hub is critical, then you can start to think about
your program like the spokes of a great wheel, spokes that hold data and functions.

So here is Rule 1:

If you want to use a class ask yourself, "Do I need a type"?
If not, don't make a class! If so, add a type to a plugin, but keep instances
either on the stack in a function or on the Hub.

Rule 2 - Dealing with Complexity
================================

The main idea of classes is that that they encapsulate functions and data, together!
Classes then can be manipulated, inherited, morphed. These concepts are beautiful,
elegant and useful. But in POP we can begin to break up the concepts of classes.

In a type, having this connection makes a lot of sense, but when it comes to programming
interfaces it becomes convoluted. We take a beautiful concept and force it to expand
beyond its bounds. This is where software complexity comes from.

All well designed code works well when it is small, it is traceable, elegant, algorithmic.
The aspects of software development is still clean and tight. We subsequently look at
code that is small and contained to be good, and monolithic, oversized and unwieldy code
to be bad.

But as complexity grows, we can't have our clean small applications, they grow with
lives of their own into sprawling and often unmaintainable codebases.

So in POP we break apart code differently, instead of encapsulating code in classes
and instances, we encapsulate functionality inside of plugin subsystems, or Subs.

Subs allow you to create functional interfaces where plugins can define functionality.
If we look at this from just a functional perspective it falls down. If we look at it
from a Flow Programming perspective it makes more sense.

Flow Programming defines functions to traverse over data, the nature of the program
transforms with the data that is sent into it.

Subs merges concepts of OOP and Flow. The Subs get created against data, system data,
configuration data. Instead of creating instances bound to data, you store data with
functions.

Rule 2 - Complexity is dealt with through breaking apart Classes. Functions work
on their own, morphed with data stored alongside them on the namespace. Instead of
encapsulation, namespace isolation.

Rule 3 - Subs and Patterns
==========================

Now that we have broken apart classes, and introduced Subs, the spokes to our Hub,
we can cover Sub Patterns.

Plugin Subs allow for the creation of new programming patterns. These patterns make
Subs amazingly flexible. Now the Subs can define programming interfaces that are
as diverse as programming itself.

Patterns include, RPC Interfaces, Data collection, Scanners, Event gatherers,
iterative processing, and simple functionality buckets and many more, some defined,
most yet to be discovered.

Rule 3 - Think of programming through exposing patterns. Patterns define the nature
of code and allow for Subs to be easy to grok, manipulate and expand. Patterns
allow for code to follow the rule of functional isolation, extending the concept
of namespace isolation.

Rule 4 - Public Vs Private
==========================

Since all of this functionality and data exist on the Hub, any other user of the
application can access it. This makes the public vs private question very serious!
When making functions, make sure they follow the chosen pattern, but maintain
all public code as if it is being used by others.

This is a good thing! Writing code that follows the rules of libraries has always
been good! So often we make private methods and data out of laziness rather than
purpose. When you choose to make something private, it should be logically only
applicable to the namespace that it is private to. Otherwise it should be public,
and developed like public code.

Rule 4 - Make functions public, unless they are truly private, and maintain them
as such. If your subs follow patterns, then they can be easily re-used, reusable
code should expose simple interfaces and follow good library development practices.

Rule 5 - App Merging
====================

Software is easier to develop and manage when it is composed of many smaller
applications. But software is easier to distribute and use when it is a single large
application. Take a Linux Distro for example, they are made of thousands of small
software packages, but these packages would be unusable alone, they need to be
glued together and distributed.

Plugin Oriented Programming is all about tearing down the walls between apps and
libs. It is designed to make apps mergeable, but also standalone and useful.

This solves the problem of communicating large codebases! Now small codebases can
be created and iterated on quickly, but still merged into a larger whole.

Rule 5 - Split your code into many smaller projects and use app merging inside of
POP to bring the small projects together into a larger merged project.
