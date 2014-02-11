#!/usr/bin/env python

from distutils.core import setup
import os
import re

version_re = re.compile(r'__version__ = "(.*)"')
cwd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(cwd, 'tellive', '__init__.py')) as init:
    for line in init:
        match = version_re.search(line)
        if match:
            version = match.group(1)
            break
    else:
        raise Exception('Cannot find version in __init__.py')

setup(
    name='tellive-py',
    version=version,
    author='Erik Johansson',
    author_email='erik@ejohansson.se',
    packages=['tellive'],
    provides=['tellive'],
    install_requires=['tellcore-py >= 1.0.3', 'oauthlib >= 0.5.1'],
    scripts=['bin/tellive_core_connector'],
    url='https://github.com/erijo/tellive-py',
    license='GPLv3+',
    description='Python wrapper for connecting to Telldus Live',
    long_description=open('README.rst').read() + '\n\n' + \
        open('CHANGES.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)
