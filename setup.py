#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

exec(open("xee/version.py").read())

setup(
    name='xee',
    version=__version__,
    packages=find_packages(),
    author='quentin7b',
    description='SDK for Xee APIs (https://dev.xee.com)',
    long_description=open('README.md').read(),
    install_requires=[
        'isodate',
        'requests'
    ],
    include_package_data=True,
    url='http://github.com/quentin7b/xee-sdk-python',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
