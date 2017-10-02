#!/usr/bin/env python

from distutils.core import setup

setup(name='PyMines',
      version='1.0.0',
      description='Very simple minesweeper game',
      author='Vilsol',
      author_email='me@vil.so',
      url='https://github.com/Vilsol/PyMines',
      packages=[
        "pymines"
      ],
      package_data={
          "pymines": ["images/*.*"]
      },
      entry_points={
          'console_scripts': [
              'pymines = pymines.pymines:execute'
          ]
      },
      )
