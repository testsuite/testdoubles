#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
from nose2.tools import such
from testdoubles.utils import are_argspecs_identical
from tests.common.layers import FunctionalTestsLayer

with such.A('keyword arguments comparison method') as it:
    it.uses(FunctionalTestsLayer)

    @it.should("return true if the argspecs are completely identical")
    def test_should_return_true_if_the_argspecs_are_completely_identical(case):
        def fake_callable1(a, k=mock.DEFAULT):
            pass

        def fake_callable2(a, k=mock.DEFAULT):
            pass

        actual = are_argspecs_identical(fake_callable1, fake_callable2)

        case.assertTrue(actual)

    @it.should(
        'return true if the argspecs are not completely identical but have the same number of positional arguments')
    def test_should_return_true_if_the_argspecs_are_not_completely_identical_but_have_the_same_number_of_positional_arguments(case):
        def fake_callable1(a):
            pass

        def fake_callable2(b):
            pass

        actual = are_argspecs_identical(fake_callable1, fake_callable2)

        case.assertTrue(actual)

    @it.should(
        'return true if the argspecs are not completely identical but the first method has a varargs argument')
    def test_should_return_true_if_the_argspecs_are_not_completely_identical_but_the_first_method_has_a_varargs_argument(case):
        def fake_callable1(*args):
            pass

        def fake_callable2(a):
            pass

        actual = are_argspecs_identical(fake_callable1, fake_callable2)

        case.assertTrue(actual)

    @it.should(
        'return true if the argspecs are not completely identical but the second method has a varargs argument')
    def test_should_return_true_if_the_argspecs_are_not_completely_identical_but_the_second_method_has_a_varargs_argument(case):
        def fake_callable1(a):
            pass

        def fake_callable2(*args):
            pass

        actual = are_argspecs_identical(fake_callable1, fake_callable2)

        case.assertTrue(actual)
        
    @it.should(
        'return false if the first method has a varargs argument and the second method has no positional arguments')
    def test_should_return_false_if_the_first_method_has_a_varargs_argument_and_the_second_method_has_no_positional_arguments(case):
        def fake_callable1(*args):
            pass

        def fake_callable2(k=mock.DEFAULT):
            pass

        actual = are_argspecs_identical(fake_callable1, fake_callable2)

        case.assertEqual(actual, False)

    @it.should(
        'return false if the first method has no positional arguments and the second method has a varargs argument')
    def test_should_return_false_if_the_first_method_has_no_positional_arguments_and_the_second_method_has_a_varargs_argument(case):
        def fake_callable1(k=mock.DEFAULT):
            pass

        def fake_callable2(*args):
            pass

        actual = are_argspecs_identical(fake_callable1, fake_callable2)

        case.assertEqual(actual, False)

    it.createTests(globals())