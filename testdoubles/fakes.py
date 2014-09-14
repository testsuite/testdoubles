#!/usr/bin/env python
# coding: utf-8
from cached_property import cached_property
import inspect
from testdoubles.utils import not_implemented


class Fake(object):
    def __init__(self, test_double, target):
        if isinstance(test_double, str):
            module, cls = test_double.rsplit('.', 1)
            self.test_double = getattr(__import__(module, fromlist=(cls, )), cls)
        else:
            self.test_double = test_double

        if isinstance(target, str):
            module, cls = target.rsplit('.', 1)
            self.target = getattr(__import__(module, fromlist=(cls, )), cls)
        else:
            self.target = target

        for unimplemented_method in self.unimplemented_methods:
            setattr(self, unimplemented_method, not_implemented(getattr(self.target, unimplemented_method)))

    @cached_property
    def unimplemented_methods(self):
        return set(dict(inspect.getmembers(self.target, predicate=inspect.ismethod)).keys()) - set(dict(
            inspect.getmembers(self.test_double, predicate=inspect.ismethod)).keys())