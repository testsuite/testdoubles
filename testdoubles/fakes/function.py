#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect


class FakeFunction(object):
    def __init__(self, live):
        self._live = live

    @property
    def live(self):
        return self._live

    @property
    def is_instance_method(self):
        try:
            args = inspect.getargspec(self.live)[0]
            is_unbound_instance_method = args[0] == 'self'
        except IndexError:
            is_unbound_instance_method = False
        return inspect.ismethod(self.live) or is_unbound_instance_method