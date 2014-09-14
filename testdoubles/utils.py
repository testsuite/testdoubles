#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps


def make_function_from_signature(f):
    pass


def bind_function_to_object(f):
    pass


def not_implemented(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        raise NotImplementedError('%s is not implemented' % f)

    return wrapper