=================
Glossary of Terms
=================

Learning Plugin Oriented Programming requires understanding a number of terms. This glossary exists
to make that easier.

`pop`: Used to reference the `pop` Python project. When specifying the `pop` implementation of
Plugin Oriented Programming use an all lowercase `pop`

`POP`: The Plugin Oriented Programming concept. When specifying the Plugin Oriented Programing paradigm
do so with all caps

`hub`: The `hub` is the root of the hierarchical namespace. The hub represents both the concept of
the hub in Plugin Oriented Programming and the hub as it is implemented in the `pop` project

`sub`: The `sub` is the implementation of the Plugin Subsystem concept of Plugin Oriented Programing
inside of `pop`

`ref`: The `ref` is a string representation of a path that can be found on the `hub`.

`pattern`: The Plugin Oriented Programming concept which defines how a Plugin Subsystem is
implemented. :ref:`sub_patterns`

`app-merging`: The ability to dynamically merge seperate POP codebases together.

`Vertical App Merging`: Extending a single plugin subsystems by defining the sub in multiple codebases.

`Horizontal App Merging`: Merging multiple subsystems together onto one hub.

`Dyne Name`: The dynamic name is used to define what plugin sub that is being defined or
extended. Dyne Names are used in Vertical App Merging.
