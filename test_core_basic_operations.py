# -*- coding: utf-8 -*-

import pytest


from core import *


def test_clear():
    empty = Stack()
    clear(Data=empty)
    assert empty.is_empty() == True

    tiny = Stack()
    tiny.push("a")
    tiny.push(1)
    clear(Data=tiny)
    assert tiny.is_empty() == True


def test_drop():
    empty = Stack()
    with pytest.raises(StackUnderflowError):
        drop(Data=empty)

    tiny = Stack()
    tiny.push("a")
    tiny.push(1)
    drop(Data=tiny)
    assert tiny.peek() == "a"


def test_swap():
    two_items = Stack()
    two_items.push("frick")
    two_items.push("frack")
    swap(Data=two_items)
    assert two_items.peek() == "frick"
    assert two_items.contents[-2] == "frack"


def test_dup():
    tiny = Stack()
    with pytest.raises(StackUnderflowError):
        dup(Data=tiny)

    tiny = Stack()
    tiny.push(1)
    dup(Data=tiny)
    assert tiny.peek() == 1
    assert tiny.contents[-2] == 1


def test_over():
    tiny = Stack()
    tiny.push(1)
    with pytest.raises(StackUnderflowError):
        over(Data=tiny)

    two_items = Stack()
    two_items.push(10)
    two_items.push(-666)
    over(Data=two_items)
    assert two_items.height() == 3
    assert two_items.pop() == 10


def test_rot():
    empty = Stack()
    with pytest.raises(StackUnderflowError):
        rot(Data=empty)

    tiny = Stack()
    tiny.push(1)
    tiny.push(2)
    tiny.push(3)
    rot(Data=tiny)
    assert tiny.height() == 3
    assert tiny.peek() == 1
    assert tiny.peek(-2) == 3
    assert tiny.peek(-3) == 2

    tiny = Stack()
    tiny.push(10)
    tiny.push(20)
    tiny.push(30)
    tiny.push(1)
    tiny.push(2)
    tiny.push(3)
    assert tiny.height() == 6
    rot(Data=tiny)
    assert tiny.height() == 6
    assert tiny.peek() == 1
    assert tiny.peek(-2) == 3
    assert tiny.peek(-3) == 2


def test_nip():
    empty = Stack()
    with pytest.raises(StackUnderflowError):
        nip(Data=empty)

    tiny = Stack()
    tiny.push(1)
    tiny.push(2)
    nip(Data=tiny)
    assert tiny.height() == 1
    assert tiny.peek() == 2

    tiny = Stack()
    tiny.push(10)
    tiny.push(20)
    tiny.push(30)
    tiny.push(1)
    tiny.push(2)
    tiny.push(3)
    nip(Data=tiny)
    assert tiny.height() == 5
    assert tiny.peek() == 3


def test_tuck():
    empty = Stack()
    with pytest.raises(StackUnderflowError):
        tuck(Data=empty)

    tiny = Stack()
    tiny.push(1)
    tiny.push(2)
    tuck(Data=tiny)
    assert tiny.height() == 3
    assert tiny.peek() == 2
    assert tiny.peek(-2) == 1
    assert tiny.peek(-3) == 2
