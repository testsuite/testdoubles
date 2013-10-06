#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RealObject(object):
    def __init__(self):
        self._real = True

    def was_faked(self):
        return False

    @property
    def real(self):
        return self._real

    @real.setter
    def real(self, value):
        self._real = value