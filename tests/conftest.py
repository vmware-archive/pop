# -*- coding: utf-8 -*-

# Import python libs
import os
import sys
import glob
import logging

CODE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if CODE_DIR in sys.path:
    sys.path.remove(CODE_DIR)
sys.path.insert(0, CODE_DIR)

# Import 3rd-party libs
import pytest


log = logging.getLogger('pop.tests')

def pytest_runtest_protocol(item, nextitem):
    '''
    implements the runtest_setup/call/teardown protocol for
    the given test item, including capturing exceptions and calling
    reporting hooks.
    '''
    log.debug('>>>>> START >>>>> {0}'.format(item.name))


def pytest_runtest_teardown(item):
    '''
    called after ``pytest_runtest_call``
    '''
    log.debug('<<<<< END <<<<<<< {0}'.format(item.name))


@pytest.fixture
def os_sleep_secs():
    if 'CI_RUN' in os.environ:
        return 1.75
    return 0.5
