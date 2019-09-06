'''
Seed a new project with a directory tree and first files
'''
# Import python libs
import os

BUILD = """#!/usr/bin/python3
import sys
import os
import shutil
import subprocess
import tempfile
import venv
import argparse

OMIT = ('__pycache__', 'PyInstaller', 'pip', 'setuptools', 'pkg_resources', '__pycache__', 'dist-info', 'egg-info')


def parse():
    '''
    Parse the cli args
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'name',
            help='The name of the script to build from the run.py')
    args = parser.parse_args()
    return args.__dict__


class Builder:
    def __init__(self):
        self.opts = parse()
        self.name = self.opts['name']
        self.cwd = os.getcwd()
        self.run = os.path.join(self.cwd, 'run.py')
        self.venv_dir = tempfile.mkdtemp(prefix='pop_', suffix='_venv')
        self.python_bin = os.path.join(self.venv_dir, 'bin', 'python')
        self.vroot = os.path.join(self.venv_dir, 'lib')
        self.all_paths = set()
        self.imports = set()
        self.datas = set()
        self.cmd = f'{self.python_bin} -B -OO -m PyInstaller '
        self.s_path = os.path.join(self.venv_dir, 'bin', self.name)
        self.pyi_args = [
              self.s_path,
              '--log-level=INFO',
              '--noconfirm',
              '--onefile',
              '--clean',
            ]

    def create(self):
        '''
        Make a virtual environment based on the version of python used to call this script
        '''
        venv.create(self.venv_dir, clear=True, with_pip=True)
        pip_bin = os.path.join(self.venv_dir, 'bin', 'pip')
        subprocess.call([pip_bin, 'install', '-r', 'requirements.txt'])
        subprocess.call([pip_bin, 'install', 'PyInstaller'])
        subprocess.call([pip_bin, '-v', 'install', self.cwd])

    def omit(self, test):
        for bad in OMIT:
            if bad in test:
                return True
        return False

    def scan(self):
        '''
        Scan the new venv for files and imports
        '''
        for root, dirs, files in os.walk(self.vroot):
            if self.omit(root):
                continue
            for d in dirs:
                full = os.path.join(root, d)
                if self.omit(full):
                    continue
                self.all_paths.add(full)
            for f in files:
                full = os.path.join(root, f)
                if self.omit(full):
                    continue
                self.all_paths.add(full)

    def to_import(self, path): 
        ret = path[path.index('site-packages') + 14:].replace(os.sep, '.')
        if ret.endswith('.py'):
            ret = ret[:-3]
        return ret

    def to_data(self, path):
        dest = path[path.index('site-packages') + 14:]
        src = path
        if not dest.strip():
            return None
        ret = f'{src}{os.pathsep}{dest}'
        return ret

    def mk_adds(self):
        '''
        make the imports and datas for pyinstaller
        '''
        for path in self.all_paths:
            if not 'site-packages' in path:
                continue
            if os.path.isfile(path):
                if not path.endswith('.py'):
                    continue
                if path.endswith('__init__.py'):
                    # Skip it, we will get the dir
                    continue
                imp = self.to_import(path)
                if imp:
                    self.imports.add(imp)
            if os.path.isdir(path):
                data = self.to_data(path)
                imp = self.to_import(path)
                if imp:
                    self.imports.add(imp)
                if data:
                    self.datas.add(data)

    def mk_cmd(self):
        '''
        Create the pyinstaller command
        '''
        for imp in self.imports:
            self.pyi_args.append(f'--hidden-import={imp}')
        for data in self.datas:
            self.pyi_args.append(f'--add-data={data}')
        for arg in self.pyi_args:
            self.cmd += f'{arg} '

    def pyinst(self):
        shutil.copy(self.run, self.s_path)
        subprocess.call(self.cmd, shell=True)

    def report(self):
        art = os.path.join(self.cwd, 'dist', self.name)
        print(f'Executable created in {art}')
        print('To create a more portable and fully static binary install run staticx against your new build')

    def clean(self):
        shutil.rmtree(self.venv_dir)
        shutil.rmtree(os.path.join(self.cwd, 'build'))
        os.remove(os.path.join(self.cwd, f'{self.name}.spec'))

    def build(self):
        self.create()
        self.scan()
        self.mk_adds()
        self.mk_cmd()
        self.pyinst()
        self.report()
        self.clean()


if __name__ == '__main__':
    builder = Builder()
    builder.build()
"""

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
    hub.pop.seed.mkbuild()


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


def mkbuild(hub):
    '''
    Create the build script to make the single executable
    '''
    path = os.path.join(hub.PATH, 'build.py')
    with open(path, 'w+') as fp:
        fp.write(BUILD)
