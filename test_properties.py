# -*- coding: utf-8 -*-

import pytest


from core import *


from hypothesis import given
from hypothesis.strategies import integers, text


@given(integers(), integers())
def test_stack_addition(x, y):
    tiny = Stack()
    tiny.push(x)
    tiny.push(y)
    add(Data=tiny)
    assert(tiny.height() == 1)
    assert(tiny.peek() == x + y)
    assert(tiny.peek() == y + x)
