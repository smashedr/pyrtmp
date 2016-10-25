from distutils.core import setup
import py2exe

setup(
    windows=[{'script': "pyrtmp.py"}],
    options={
        'py2exe': {
            'compressed': True
        }
    },
    zipfile=None,
)
