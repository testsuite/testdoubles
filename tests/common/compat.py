#!/usr/bin/env python
# -*- coding: utf-8 -*-
import six
import sys

try:
    from unittest import mock
except ImportError:
    import mock

if not six.PY3 and sys.version_info[1] == 6:
        import unittest2 as unittest
else:
    try:
        import unittest
    except ImportError:
        import unittest2 as unittest

__all__ = ['mock', 'unittest']