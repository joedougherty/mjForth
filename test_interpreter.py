# -*- coding: utf-8 -*-

import pytest


from mjForth import execute_lines, Data


def test_simple():
    execute_lines('2 2 add')
    assert(Data.height() == 1)
    assert(Data.peek() == 4)
    
    execute_lines('2 2 add')
    execute_lines('add') # <2> 4 4
    assert(Data.height() == 1)
    assert(Data.peek() == 8)
