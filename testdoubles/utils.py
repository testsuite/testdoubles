#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect


def are_argspecs_identical(callable1, callable2):
    argspec1 = inspect.getargspec(callable1)
    argspec2 = inspect.getargspec(callable2)

    return argspec1 == argspec2

__all__ = ('are_argspecs_identical', )