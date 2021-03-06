# -*- coding: utf-8 -*-

import pytest


from core import *
from mjForth import run


from hypothesis import given
from hypothesis.strategies import integers, floats, one_of


nums = one_of(
    integers(), 
    floats(allow_nan=False, allow_infinity=False)
)


@given(nums, nums)
def test_stack_addition(x, y):
    tiny = Stack()
    tiny.push(x)
    tiny.push(y)
    add(Data=tiny)
    assert tiny.height() == 1
    assert tiny.peek() == x + y
    assert tiny.peek() == y + x


@given(nums, nums)
def test_stack_subtraction(x, y):
    tiny = Stack()
    tiny.push(x)
    tiny.push(y)
    subtract(Data=tiny)
    assert tiny.height() == 1
    assert tiny.peek() == x - y


@given(nums, nums)
def test_addition_interpreter(x, y):
    code = f'''{x} {y} +'''
    run(code)
    top_of_stack = Data.peek()
    assert top_of_stack == x + y


@given(nums, nums)
def test_subtraction_interpreter(x, y):
    code = f'''{x} {y} - '''
    run(code)
    top_of_stack = Data.peek()
    assert top_of_stack == x - y


@given(nums, nums)
def test_swap_interpreter(x, y):
    code = f'''{x} {y} swap'''
    run(code)
    top_of_stack, just_below = Data.peek(), Data.peek(-2)
    assert top_of_stack == x
    assert just_below == y
    
