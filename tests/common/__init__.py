#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def is_executing_under_continuous_integration_server():
    return os.getenv('CI', 'false') == 'true'