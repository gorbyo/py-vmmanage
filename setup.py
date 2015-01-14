#!/usr/bin/env python2
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

setup(
    name='py_vmmanage',
    version='0.2',
    description='Short description',
    long_description=''.join(open('README.rst').readlines()),
    keywords='vmware, cobbler',
    author='Oleh Horbachov',
    author_email='gorbyo@gmail.com',
    license='GPLv2',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        ],
    requires=['pysphere']
)
