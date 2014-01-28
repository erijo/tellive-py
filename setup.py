#!/usr/bin/env python

from distutils.core import setup

setup(
    name='tellive-py',
    version='0.1.0',
    author='Erik Johansson',
    author_email='erik@ejohansson.se',
    packages=['tellive'],
    provides=['tellive'],
    requires=['tellcore (>= 1.0)'],
    scripts=['bin/tellive_core_connector'],
    url='https://github.com/erijo/tellive-py',
    license='GPLv3+',
    description='Python wrapper for connecting to Telldus Live',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Home Automation',
        ],
)
