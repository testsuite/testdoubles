#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
from nose2.tools import such
from testdoubles.utils import are_arguments_identical
from tests.common.layers import UnitTestsLayer

with such.A('arguments comparison method') as it:
    it.uses(UnitTestsLayer)

    @it.should("return true if the first method has an argument and the second method has specified a varargs argument")
    def test_should_return_true_if_the_first_method_has_an_argument_and_the_second_method_has_specified_a_varargs_argument(
            case):
        actual = are_arguments_identical(inspect.ArgSpec(['a'], None, None, None),
                                         inspect.ArgSpec([], 'args', None, None))

        case.assertTrue(actual)

    @it.should(
        "return true if the first method has specified a varargs argument and the second method has an argument ")
    def test_should_return_true_if_the_first_method_has_specified_a_varargs_argument_and_the_second_method_has_an_argument(
            case):
        actual = are_arguments_identical(inspect.ArgSpec([], 'args', None, None),
                                         inspect.ArgSpec(['a'], None, None, None))

        case.assertTrue(actual)

    @it.should("return true if both methods have the same amount of arguments")
    def test_should_return_true_if_both_methods_have_the_same_amount_of_arguments(case):
        actual = are_arguments_identical(inspect.ArgSpec(['a'], None, None, None),
                                         inspect.ArgSpec(['a'], None, None, None))

        case.assertTrue(actual)

    @it.should("return false if the first method doesn't have the same amount of arguments as the second")
    def test_should_return_true_if_both_methods_have_the_same_amount_of_arguments(case):
        actual = are_arguments_identical(inspect.ArgSpec(['a', 'b'], None, None, None),
                                         inspect.ArgSpec(['a'], None, None, None))

        case.assertEqual(actual, False)

    @it.should("return false if the second method doesn't have the same amount of arguments as the first")
    def test_should_return_true_if_both_methods_have_the_same_amount_of_arguments(case):
        actual = are_arguments_identical(inspect.ArgSpec(['a'], None, None, None),
                                         inspect.ArgSpec(['a', 'b'], None, None, None))

        case.assertEqual(actual, False)

    it.createTests(globals())