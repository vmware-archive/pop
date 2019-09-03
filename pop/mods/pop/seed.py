'''
Seed a new project with a directory tree and first files
'''
# Import python libs
import os


SETUP = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import python libs
import os
import sys
import shutil
from setuptools import setup, Command

NAME = '%%NAME%%'
DESC = ('')

# Version info -- read without importing
_locals = {}
with open('{}/version.py'.format(NAME)) as fp:
    exec(fp.read(), None, _locals)
VERSION = _locals['version']
SETUP_DIRNAME = os.path.dirname(__file__)
if not SETUP_DIRNAME:
    SETUP_DIRNAME = os.getcwd()


class Clean(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for subdir in (NAME, 'tests'):
            for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), subdir)):
                for dir_ in dirs:
                    if dir_ == '__pycache__':
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    for package in (NAME, ):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, '.')
            modules.append(modname)
    return modules


setup(name=NAME,
      author='',
      author_email='',
      url='',
      version=VERSION,
      description=DESC,
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Development Status :: 5 - Production/Stable',
          ],
      entry_points={
        'console_scripts': [
            '%%NAME%% = %%NAME%%.scripts:start',
            ],
          },
      packages=discover_packages(),
      cmdclass={'clean': Clean},
      )
'''

SCRIPT = '''#!/usr/bin/env python3
import pop.hub

def start():
    hub = pop.hub.Hub()
    hub.pop.sub.add('%%NAME%%.%%NAME%%')
'''

INIT = '''def __init__(hub):
    print('%%NAME%% works!')
'''

REQ = 'pop'

CONF = '''CLI_CONFIG = {}
CONFIG = {}
GLOBAL = {}
SUBS = {}
'''

VER = '''# All pop projects follow semantic versioning version 2.0.0: https://semver.org/
version = '1.0.0'
'''


def new(hub):
    '''
    Given the option in hub.opts "seed_name" create a directory tree for a
    new pop project
    '''
    hub.PATH = os.getcwd()
    name = hub.opts['seed_name']
    hub.pop.seed.mkdir(name, name)
    hub.pop.seed.mkdir(name, name, 'contracts')
    hub.pop.seed.mksetup(name)
    hub.pop.seed.mkscript(name)
    hub.pop.seed.mkrun(name)
    hub.pop.seed.mkinit(name)
    hub.pop.seed.mkversion(name)
    hub.pop.seed.mkconf(name)
    hub.pop.seed.mkreq(name)


def mkdir(hub, *args):
    '''
    Create the named dir
    '''
    path = hub.PATH
    for dir_ in args:
        path = os.path.join(path, dir_)
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except Exception:
                print('Failed to make {}'.format(path))
                continue
            if dir_ == 'scripts' and len(args) == 1:
                continue


def mkreq(hub, name):
    '''
    '''
    path = os.path.join(hub.PATH, 'requirements.txt')
    with open(path, 'w+') as fp:
        fp.write(REQ)


def mksetup(hub, name):
    '''
    Create and write out a setup.py file
    '''
    path = os.path.join(hub.PATH, 'setup.py')
    setup_str = SETUP.replace('%%NAME%%', name)
    with open(path, 'w+') as fp:
        fp.write(setup_str)


def mkscript(hub, name):
    '''
    Create and write out a setup.py file
    '''
    path = os.path.join(hub.PATH, name, 'scripts.py')
    script_str = SCRIPT.replace('%%NAME%%', name)
    with open(path, 'w+') as fp:
        fp.write(script_str)


def mkrun(hub, name):
    '''
    Create the convenience run.py script allowing the project to
    be executed from the local directory
    '''
    path = os.path.join(hub.PATH, 'run.py')
    run_str = SCRIPT.replace('%%NAME%%', name)
    run_str += '\n\nstart()'
    with open(path, 'w+') as fp:
        fp.write(run_str)


def mkinit(hub, name):
    '''
    Create the intial init.py
    '''
    path = os.path.join(hub.PATH, name, name, 'init.py')
    init_str = INIT.replace('%%NAME%%', name)
    with open(path, 'w+') as fp:
        fp.write(init_str)


def mkversion(hub, name):
    '''
    Create the version.py file
    '''
    path = os.path.join(hub.PATH, name, 'version.py')
    with open(path, 'w+') as fp:
        fp.write(VER)


def mkconf(hub, name):
    '''
    Create the version.py file
    '''
    path = os.path.join(hub.PATH, name, 'conf.py')
    with open(path, 'w+') as fp:
        fp.write(CONF)
