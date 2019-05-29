# -*- coding: utf-8 -*-
'''
Pop related exceptions
'''


class PopBaseException(Exception):
    '''
    Base exception where all of Pop's exceptions derive
    '''


class PopError(PopBaseException):
    '''
    General purpose pack exception to signal an error
    '''


class PopLoadError(PopBaseException):
    '''
    Exception raised when a pack module fails to load
    '''


class PopLookupError(PopBaseException):
    '''
    Exception raised when a pack module lookup fails
    '''


class ContractModuleException(PopBaseException):
    '''
    Exception raised when a function specified in a contract as required
    to exist is not found in the loaded module
    '''


class ContractFuncException(PopBaseException):
    '''
    Exception raised when a function specified in a contract as required
    to exist is found on the module but it's not function
    '''


class ProcessNotStarted(PopBaseException):
    '''
    Exception raised when failing to start a process on the process manager
    '''


class BindError(PopBaseException):
    '''
    Exception raised when arguments for a function in a ContractedContext cannot be bound
    Indicates invalid function arguments.
    '''
