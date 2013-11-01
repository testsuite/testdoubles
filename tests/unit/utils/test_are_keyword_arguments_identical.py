#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import mock
from nose2.tools import such
from testdoubles.utils import are_keyword_arguments_identical
from tests.common.layers import UnitTestsLayer

with such.A('keyword arguments comparison method') as it:
    it.uses(UnitTestsLayer)

    @it.should(
        "return true if the first method has a keyword argument and the second method has specified a kwargs argument")
    def test_should_return_true_if_the_first_method_has_a_keyword_argument_and_the_second_method_has_specified_a_kwargs_argument(
            case):
        actual = are_keyword_arguments_identical(inspect.ArgSpec(['a'], None, None, (mock.DEFAULT, )),
                                                 inspect.ArgSpec([], None, 'kwargs', None))

        case.assertTrue(actual)

    @it.should(
        "return true if the first method has specified a kwargs argument and the second method has a keyword argument")
    def test_should_return_true_if_the_first_method_has_specified_a_kwargs_argument_and_the_second_method_has_a_keyword_argument(
            case):
        actual = are_keyword_arguments_identical(inspect.ArgSpec([], None, 'kwargs', None),
                                                 inspect.ArgSpec(['a'], None, None, (mock.DEFAULT, )))

        case.assertTrue(actual)

    it.createTests(globals())