#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RealObject(object):
    def was_faked(self):
        return False

    @property
    def real(self):
        return True

    @real.setter
    def real(self, value):
        pass