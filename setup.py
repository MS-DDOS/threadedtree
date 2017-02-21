'''
This file is part of Threadedtree.

Threadedtree is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Threadedtree is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with threadedtree.  If not, see <http://www.gnu.org/licenses/>.
'''

from distutils.core import setup
from setuptools import find_packages

setup(
    name='ThreadedTree',
    version='1.0dev',
    author="M Tyler Springer",
    author_email="mspringer@smu.edu",
    url="http://tylerspringer.com/",
    packages=find_packages(),
    license='GNU Lesser General Public License v3.0',
    description='A carefully implemented double threaded binary search tree in pure python.',
    test_suite='nose.collector',
    tests_require=['nose','coverage']
    )
