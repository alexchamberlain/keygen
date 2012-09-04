#!/usr/bin/python2
from __future__ import with_statement
import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):
  pip   = os.path.join(home_dir, 'bin', 'pip')
  subprocess.call([pip, 'install', 'flask'])
  subprocess.call([pip, 'install', 'pyopenssl'])
"""))

with open('bootstrap.py', 'w') as f:
  f.write(output)
