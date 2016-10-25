from distutils.core import setup
import py2exe

setup(
    windows=[{'script': "pyrtmp.py"}],
    options={
        'py2exe': {
            'includes': ['tkinter'],
            'bundle_files': 2,
            'compressed': True
        },
    },
    zipfile=None,
)
