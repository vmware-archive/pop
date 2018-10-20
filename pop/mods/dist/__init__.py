'''
The dist subsystem is used to create, deploy, and manage distributable
software subsystems. it provides packaging, validation, versioning,
building, compressing and signing
'''
# Definition of the package
#   Support naming, versioning, deps (subs and python)
#   Defined within a python file
#   Define initialization of the package within an existing hub
#   Define extra files to be included
#   create compressed tarball for delivery
#   Allow for signing the package
#   Create validation of signitures and of checksums