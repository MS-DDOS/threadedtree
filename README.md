# threadedtree 
![Build Status](https://travis-ci.org/MS-DDOS/threadedtree.svg?branch=master) [![Coverage Status](https://coveralls.io/repos/github/MS-DDOS/threadedtree/badge.svg?branch=master)](https://coveralls.io/github/MS-DDOS/threadedtree?branch=master) [![PyPI version](https://badge.fury.io/py/ThreadedTree.svg)](https://badge.fury.io/py/ThreadedTree)

A carefully implemented double threaded binary search tree in pure python.

Package is now in a stable state and is safe to inherit from to create variations such as a threaded AVL tree or a threaded red/black tree. Both of which are on the TODO list.

Complete API Documentation coming soon...

To run tests navigate to package root and execute:

`pip install nose`

`pip install coverage`

`nosetests`

For coverage status you can run `nosetest` with the following options:

`nosetests --with-coverage --cover-tests --cover-erase --cover-html`

In this example the `--cover-html` option is invoked, so a new directory `cover/` will be generated. Open `cover/index.html` in your favorite browser for a more in depth report.
Note that the option `--cover-tests` also performs a coverage report on the tests themselves (this is generally a good idea).
