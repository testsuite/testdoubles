===========
testdoubles
===========

.. image:: https://pypip.in/v/testdoubles/badge.png
    :target: https://crate.io/packages/testdoubles?version=latest
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/testdoubles/badge.png
    :target: https://crate.io/packages/testdoubles?version=latest
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/testsuite/testdoubles.png?branch=master
    :target: https://travis-ci.org/testsuite/testdoubles
    :alt: Build Status

.. image:: https://coveralls.io/repos/testsuite/testdoubles/badge.png?branch=master
    :target: https://coveralls.io/r/testsuite/testdoubles?branch=master
    :alt: Coverage Status

.. image:: https://www.versioneye.com/python/testdoubles/badge.png
    :target: http://www.versioneye.com/python/testdoubles/
    :alt: Dependencies Status


testdoubles is a testing framework for python that provides `test doubles`_.


.. image:: http://img.shields.io/license/bsd3.png?color=green
    :target: https://github.com/testsuite/testdoubles/blob/master/LICENSE
    :alt: BSD3 license
.. image:: http://b.repl.ca/v1/readthedocs-documentation-blue.png
    :target: http://testdoubles.rtfd.org.
    :alt: Documentation

.. note:: This is work in progress!

Overview
========

testdoubles provides mocks, fakes, stubs and dummies according to the definition by `Martin Fowler`_ although
`Jeff Atwood`_ provides a much more vivid definition and mechanisms for substituting objects with test doubles in
a reliable fashion without modifying the code under test.

+++++++++
Rationale
+++++++++

The standard `mock library`_ (available from Python 3.3 and as a `separate library`_) is a great tool for isolating the
system under test but it has limitations which testdoulbes lifts and idiosyncrasies which testdoubles removes.

Where to patch
--------------

You need to know `where to patch`_.

If you want to patch an object, you have to do so in the module where it's **imported into** and not the module it's
**imported from**. `Alex Marandon`_ explains it quite well.

This limitation completely violates the `Zen of Python`_:

*   "Complex is better than complicated." - mock unnecessarily makes patching complicated when there are (complex)
    solutions available to lift this limitation.
*   "There should be one-- and preferably only one --**obvious** way to do it." -
    mock does not make patching obvious.

One objects to rule them all
----------------------------

mock has only one object, `Mock`_ that is being used for substituting the dependencies of the system under test.
Since different test doubles have different purposes the distinction is important.

The distinction improves the test code readability and clarifies what exactly is being tested and how.
The distinction also prevents mixing different kinds of test doubles which reduces the mental strain when writing tests.

++++++++
Features
++++++++

* Complete API compatibility with mock (testdoubles can be used as a drop in replacement so you're old tests will
 still work).
* Patching of the dependency and not the call site.
* Completely non-intrusive to the code under test.
* Minimally intrusive to the testing code.
* Mock Objects
* Stub Objects
* Fake Objects
* Dummy Objects

Contributing
------------

.. image:: https://badge.waffle.io/testsuite/testdoubles.png?label=ready
    :target: http://waffle.io/testsuite/testdoubles
    :alt: Stories in Ready

See CONTRIBUTING.rst for details.

.. _test doubles: http://xkcd.com/703/
.. _Martin Fowler: http://martinfowler.com/articles/mocksArentStubs.html#TheDifferenceBetweenMocksAndStubs
.. _Jeff Atwood: http://www.codinghorror.com/blog/2007/01/test-doubles-a-taxonomy-of-pretend-objects.html
.. _mock library: http://docs.python.org/3.3/library/unittest.mock
.. _separate library: http://www.voidspace.org.uk/python/mock/
.. _where to patch: http://www.voidspace.org.uk/python/mock/patch.html#where-to-patch
.. _Alex Marandon: http://alexmarandon.com/articles/python_mock_gotchas/#patching-in-the-wrong-place
.. _Zen of Python: http://www.python.org/dev/peps/pep-0020/
.. _Mock: http://docs.python.org/dev/library/unittest.mock#magicmock-and-magic-method-support