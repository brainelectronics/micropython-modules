#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup
import pathlib
import sdist_upip

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# load elements of version.py
exec(open(here / 'be_helpers' / 'version.py').read())

setup(
    name='micropython-brainelectronics-helpers',
    version=__version__,
    description="MicroPython brainelectronics helpers library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/brainelectronics/micropython-modules',
    author='brainelectronics',
    author_email='info@brainelectronics.de',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: MicroPython',
    ],
    keywords='micropython, brainelectronics, modules, library',
    project_urls={
        'Bug Reports': 'https://github.com/brainelectronics/micropython-modules/issues',
        'Source': 'https://github.com/brainelectronics/micropython-modules',
    },
    license='MIT',
    cmdclass={'sdist': sdist_upip.sdist},
    packages=['be_helpers'],
    install_requires=[]
)
