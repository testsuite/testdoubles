#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from unittest import mock
except ImportError:
    import mock

try:
    import unittest
except ImportError:
    import unittest2 as unittest

__all__ = ['mock']