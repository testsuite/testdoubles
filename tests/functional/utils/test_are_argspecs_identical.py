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

    it.createTests(globals())