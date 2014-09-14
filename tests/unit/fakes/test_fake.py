#!/usr/bin/env python
# coding: utf-8
from unittest import TestCase

from testdoubles.fakes import Fake
from tests.unit.fakes.support import RealObject, EmptyFake


class FakeTestCase(TestCase):
    def test_when_providing_a_string_that_is_a_valid_import_path_the_target_object_is_imported(self):
        sut = Fake(EmptyFake, 'tests.unit.fakes.support.RealObject')

        self.assertEqual(sut.target, RealObject)

    def test_when_providing_a_string_that_is_an_invalid_import_path_an_import_error_is_raised(self):
        with self.assertRaises(ImportError):
            sut = Fake(EmptyFake, 'some.fake.Path')
            
    def test_when_providing_a_string_that_is_a_valid_import_path_the_test_double_object_is_imported(self):
        sut = Fake('tests.unit.fakes.support.EmptyFake', RealObject)

        self.assertEqual(sut.test_double, EmptyFake)

    def test_when_providing_a_string_that_is_an_invalid_import_to_the_test_double_path_an_import_error_is_raised(self):
        with self.assertRaises(ImportError):
            sut = Fake('some.fake.Path', RealObject)

    def test_when_not_implementing_foo_it_will_appear_on_the_not_implemented_list_of_the_fake_object(self):
        sut = Fake(EmptyFake, 'tests.unit.fakes.support.RealObject')

        actual = sut.unimplemented_methods
        self.assertIn('foo', actual)

    def test_when_calling_a_non_implemented_method_foo_on_the_fake_object_it_will_raise_an_unimplemented_error(self):
        sut = Fake(EmptyFake, 'tests.unit.fakes.support.RealObject')

        with self.assertRaises(NotImplementedError):
            sut.foo()