# -*- coding: utf-8 -*-

import pytest


from core import *


def test_clear():
    empty = Stack()
    clear(Data=empty)
    assert(empty.is_empty() == True)

    tiny = Stack()
    tiny.push('a')
    tiny.push(1)
    clear(Data=tiny)
    assert(tiny.is_empty() == True)


def test_drop():
    tiny = Stack()
    tiny.push('a')
    tiny.push(1)
    drop(Data=tiny)
    assert(tiny.peek() == 'a')

    empty = Stack()
    with pytest.raises(IndexError):
        drop(Data=empty)


def test_swap():
    two_items = Stack()
    two_items.push('frick')
    two_items.push('frack')
    swap(Data=two_items)
    assert(two_items.peek() == 'frick')
    assert(two_items.contents[-2] == 'frack')