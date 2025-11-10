'''
    custom build integration for setuptools 
    compiles C extensions via Makefile.
'''

import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


class BuildWithMake(build_py):
    '''
        Extends setuptools' build_py command to compile C extensions.
        Overrides the run() method to inject C compilation via make before
        standard run completes.
    '''
    
    def run(self):
        '''
            Execute the build processes
            compile C code then build Python package.
        '''
        subprocess.check_call(['make'])
        super().run()

setup(
    cmdclass={
        'build_py': BuildWithMake,  # Replace default build_py with mine.
    }
)
