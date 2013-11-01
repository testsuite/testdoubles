#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect


def are_arguments_identical(argspec1, argspec2):
    if len(argspec1[0]) == len(argspec2[0]):
        return True
    elif any(_ for _ in argspec1[0]) and argspec2[1] or any(_ for _ in argspec2[0]) and argspec1[1]:
        return True

    return False


def are_keyword_arguments_identical(argspec1, argspec2):
    pass


def are_argspecs_identical(callable1, callable2):
    argspec1 = inspect.getargspec(callable1)
    argspec2 = inspect.getargspec(callable2)

    if argspec1 == argspec2:
        return True
    else:
        return are_arguments_identical(argspec1, argspec2) and are_keyword_arguments_identical(argspec1, argspec2)

__all__ = ('are_argspecs_identical', )