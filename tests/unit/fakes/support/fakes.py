#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock


def fake_live_bound_callable():
    mocked_callable = mock.MagicMock()
    self = mock.PropertyMock()
    type(mocked_callable).__self__ = self
    mocked_callable.__name__ = 'fake_live_bound_callable'
    return mocked_callable, self


def fake_live_unbound_callable():
    mocked_callable = mock.MagicMock()
    self = mock.PropertyMock()
    self.return_value = None
    type(mocked_callable).__self__ = self
    return mocked_callable, self