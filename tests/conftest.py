# -*- coding: utf-8 -*-

# Import python libs
import os
import sys
import glob
import logging

SCRIPTS_CODE_DIR = CODE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
COMPILED_SOURCES = '--compiled' in sys.argv or '-C' in sys.argv


def compile_sources():
    # We're changing a global variable, state it so
    global SCRIPTS_CODE_DIR

    BUILD_LIBS_PATHS = glob.glob(os.path.join(CODE_DIR, 'build', 'lib.*', '*'))
    if BUILD_LIBS_PATHS and 'SKIP_SOURCES_COMPILATION' in os.environ:
        # Don't recompile if told not to and compiled sources exist but update the SCRIPTS_CODE_DIR
        SCRIPTS_CODE_DIR = os.path.dirname(BUILD_LIBS_PATHS[0])

        # Let's inject the compiled C libraries in PATH
        sys.path.insert(0, SCRIPTS_CODE_DIR)

        if CODE_DIR in sys.path:
            sys.path.remove(CODE_DIR)
        return

    sys.stderr.write('Compiling sources ... \n')
    sys.stderr.flush()

    # Let's compile them
    import subprocess
    import multiprocessing
    try:
        subprocess.check_call(
            [sys.executable,
             'setup.py',
             '--concurrency={}'.format(multiprocessing.cpu_count()),
             'build'
            ], cwd=CODE_DIR)
        sys.stderr.write('DONE\n')
        sys.stderr.flush()
        BUILD_LIBS_PATHS = glob.glob(os.path.join(CODE_DIR, 'build', 'lib.*', '*'))
    except subprocess.CalledProcessError:
        sys.stderr.write('FAILED\n')
        sys.stderr.flush()
        # Let's not leave a half built 'build/' directory around
        try:
            subprocess.check_call(
                [sys.executable, 'setup.py', 'clean', '-a'],
                cwd=CODE_DIR
            )
        except subprocess.CalledProcessError:
            pass
        sys.exit(1)

    SCRIPTS_CODE_DIR = os.path.dirname(BUILD_LIBS_PATHS[0])

    # Let's inject the compiled C libraries in PATH
    sys.path.insert(0, SCRIPTS_CODE_DIR)

    if CODE_DIR in sys.path:
        sys.path.remove(CODE_DIR)


if COMPILED_SOURCES:
    compile_sources()
if CODE_DIR in sys.path:
    sys.path.remove(CODE_DIR)
sys.path.insert(0, CODE_DIR)

# Import 3rd-party libs
import pytest


log = logging.getLogger('pop.tests')


def pytest_addoption(parser):
    '''
    register argparse-style options and ini-style config values.
    '''
    parser.addoption(
        '--compiled', '-C',
        action='store_true',
        help='Run the test suite against the C compiled sources'
    )


@pytest.hookimpl(trylast=True)
def pytest_generate_tests(metafunc):
    if 'test_run_type' not in metafunc.fixturenames:
        metafunc.fixturenames.insert(0, 'test_run_type')
        test_run_type_params = ['Cython' if metafunc.config.option.compiled else 'Python']
        test_run_type_ids = ['TestRunType({})'.format(test_run_type_params[0])]
        metafunc.parametrize(
            'test_run_type',
            test_run_type_params,
            ids=test_run_type_ids,
            scope='function'
        )


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
