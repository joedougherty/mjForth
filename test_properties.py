# -*- coding: utf-8 -*-

import pytest


from core import *


from hypothesis import given
from hypothesis.strategies import integers, floats, one_of


nums = one_of(
    integers(), 
    floats(allow_nan=False, allow_infinity=False)
)


@given(nums, nums)
def test_stack_addition_ints(x, y):
    tiny = Stack()
    tiny.push(x)
    tiny.push(y)
    add(Data=tiny)
    assert tiny.height() == 1
    assert tiny.peek() == x + y
    assert tiny.peek() == y + x


@given(nums, nums)
def test_stack_subtraction_ints(x, y):
    tiny = Stack()
    tiny.push(x)
    tiny.push(y)
    subtract(Data=tiny)
    assert tiny.height() == 1
    assert tiny.peek() == x - y
