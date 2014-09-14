#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from testdoubles.utils import not_implemented


class NotImplementedWrapperTestCase(TestCase):
    def test_when_calling_a_wrapped_function_with_the_not_implemented_decorator_a_not_implemented_error_is_raised(self):
        def f():
            pass

        sut = not_implemented(f)

        with self.assertRaises(NotImplementedError):
            sut()

    def test_when_calling_a_wrapped_function_with_the_not_implemented_decorator_the_not_implemented_error_message_is_correct(self):
        def f():
            pass

        sut = not_implemented(f)

        with self.assertRaisesRegexp(NotImplementedError, '%s is not implemented' % f):
            sut()