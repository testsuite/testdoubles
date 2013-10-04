#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose2.tools import such
from mockingbird import fake

with such.A('Fake Object') as it:
    @it.should('raise a TypeError when the configuration does not exist')
    def test_should_raise_type_error_when_configuration_does_not_exist(case):
        with case.assertRaisesRegexp(TypeError, 'A fake testdouble must have a Configuration class.'):
            fake(object)

    it.createTests(globals())
