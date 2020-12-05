# -*- coding: utf-8 -*-

import pytest


from mjForth import execute_lines, Data


def test_simple():
    execute_lines('2 2 add')
    assert(Data.height() == 1)
    assert(Data.peek() == 4)
