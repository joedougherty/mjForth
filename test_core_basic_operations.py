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
