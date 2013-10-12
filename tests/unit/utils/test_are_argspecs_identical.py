#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
from nose2.tools import such
from testdoubles.utils import are_argspecs_identical
from tests.common.layers import UnitTestsLayer
from tests.common.compat import mock

with such.A('Arguments comparison method') as it:
    it.uses(UnitTestsLayer)

    @it.should("return true if the argspecs are completely identical")
    def test_should_return_true_if_the_argspecs_are_completely_identical(case):
        with mock.patch('inspect.getargspec', return_value=mock.DEFAULT):
            actual = are_argspecs_identical(mock.DEFAULT, mock.DEFAULT)

        case.assertTrue(actual)

    @it.should("return false if the argspecs are completely different")
    def test_should_return_true_if_the_argspecs_are_completely_identical(case):
        def fake_getargspec(_):
            return getattr(mock.sentinel, random.choice(string.ascii_letters))

        with mock.patch('inspect.getargspec', fake_getargspec):
            actual = are_argspecs_identical(mock.DEFAULT, mock.DEFAULT)

        case.assertEqual(actual, False)

    it.createTests(globals())