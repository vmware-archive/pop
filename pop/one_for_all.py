#!/usr/bin/python3
import sys
import os
import shutil
import subprocess
import tempfile
import venv

cwd = os.getcwd()

# Make a virtual environment based on the version of python used to call this script
virtualenv_dir = tempfile.mkdtemp(prefix='pop_', suffix='_venv')
venv.create(virtualenv_dir, clear=True, with_pip=True)
python_bin = os.path.join(virtualenv_dir, 'bin', 'python')
pip_bin = os.path.join(virtualenv_dir, 'bin', 'pip')

# Install dependencies
subprocess.Popen([pip_bin, 'install', '-r', 'requirements.txt']).wait()
subprocess.Popen([pip_bin, 'install', 'PyInstaller']).wait()
subprocess.Popen([pip_bin, '-v', 'install', cwd]).wait()

# Run pyinstaller from the virtual environment to create the script
subprocess.Popen([os.path.join(virtualenv_dir, 'bin', 'pyinstaller'), os.path.join(virtualenv_dir, 'bin', 'heis'),
                  # PyInstaller options
                  '--log-level=INFO',
                  '--noconfirm',
                  '--hidden-import=pop',
                  '--hidden-import=pop.mods',
                  '--hidden-import=pop.mods.pop',
                  #'--onefile',
                  f'--paths={cwd}',
                  '--clean',
                  ] + sys.argv[1:]).wait()

print('Executable created in {}'.format(os.path.join(cwd, 'dist', 'heis')))

print(virtualenv_dir)
#shutil.rmtree(virtualenv_dir)
