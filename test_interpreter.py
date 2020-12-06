# -*- coding: utf-8 -*-

import pytest


from mjForth import execute_lines, Data, Memory


def test_simple():
    execute_lines("2 2 add")
    assert Data.height() == 1
    assert Data.peek() == 4

    execute_lines("2 2 add")
    execute_lines("add")  # <2> 4 4
    assert Data.height() == 1
    assert Data.peek() == 8


def test_simple_2():
    Data.clear()
    assert Data.height() == 0

    execute_lines("2 66 swap")
    assert Data.height() == 2
    assert Data.peek() == 2
    assert Data.peek(-2) == 66


def test_simple_3():
    Data.clear()
    assert Data.height() == 0

    execute_lines("666666666666666666666666666666666666 1 max")
    assert Data.height() == 1
    assert Data.peek() == 666666666666666666666666666666666666

    execute_lines("666666666666666666666666666666666666 1 min")
    assert Data.peek() == 1


def test_variable():
    Data.clear()

    execute_lines("variable test")
    assert Memory["test"] == None

    execute_lines("37 test !")
    assert Memory["test"] == 37

    execute_lines("370101013 test !")
    assert Memory["test"] == 370101013

    Data.clear()
    execute_lines("13")
    execute_lines("test !")
    assert Memory["test"] == 13


def test_word():
    Data.clear()

    execute_lines(
        " : fac_rec ( n -- n! ) dup 0> IF dup 1- fac_rec * ELSE drop 1 ENDIF ;"
    )
    execute_lines("6 fac_rec")
    assert Data.height() == 1
    assert Data.peek() == 720
