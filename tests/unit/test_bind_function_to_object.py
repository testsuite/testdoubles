#!/usr/bin/env python
# coding: utf-8
from unittest import TestCase

from testdoubles.utils import bind_function_to_object
from tests.common.compat import mock


class BindFunctionToObjectTestCase(TestCase):
    def test_when_binding_a_function_to_an_object_it_is_available_for_the_object_instance(self):
        def f(self):
            pass

        class Obj(object):
            pass

        bind_function_to_object(f, Obj)

        sut = Obj()

        self.assertTrue(hasattr(sut, 'f'), 'Obj has no attribute f')

    def test_when_binding_a_function_to_an_object_it_is_callable_on_the_object_instance(self):
        def f(self):
            pass

        class Obj(object):
            pass

        bind_function_to_object(f, Obj)

        sut = Obj()

        sut.f()

    def test_when_binding_a_function_to_an_object_then_the_object_is_returned(self):
        def f(self):
            pass

        class Obj(object):
            pass

        actual = bind_function_to_object(f, Obj)

        self.assertEqual(actual, Obj)

    def test_when_providing_a_non_callable_a_type_error_is_raised(self):
        class Obj(object):
            pass

        with self.assertRaises(TypeError):
            bind_function_to_object(mock.sentinel, Obj)

    def test_when_providing_a_non_boundable_function_a_value_error_is_raised(self):
        def f():
            pass

        class Obj(object):
            pass

        with self.assertRaises(ValueError):
            bind_function_to_object(f, Obj)

    def test_when_providing_a_non_boundable_function_then_the_value_error_message_is_correct(self):
        def f():
            pass

        class Obj(object):
            pass

        with self.assertRaisesRegexp(ValueError, '%s does not have a self argument' % f):
            bind_function_to_object(f, Obj)