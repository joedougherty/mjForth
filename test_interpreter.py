# -*- coding: utf-8 -*-

import pytest


from mjForth import run, Data, Memory, execute_file


def test_simple():
    run("2 2 add")
    assert Data.height() == 1
    assert Data.peek() == 4

    run("2 2 add")
    run("add")  # <2> 4 4
    assert Data.height() == 1
    assert Data.peek() == 8


def test_simple_2():
    Data.clear()
    assert Data.height() == 0

    run("2 66 swap")
    assert Data.height() == 2
    assert Data.peek() == 2
    assert Data.peek(-2) == 66


def test_simple_3():
    Data.clear()
    assert Data.height() == 0

    run("666666666666666666666666666666666666 1 max")
    assert Data.height() == 1
    assert Data.peek() == 666666666666666666666666666666666666

    run("666666666666666666666666666666666666 1 min")
    assert Data.peek() == 1


def test_variable():
    Data.clear()

    run("variable test")
    assert Memory["test"] == None

    run("37 test !")
    assert Memory["test"] == 37

    run("370101013 test !")
    assert Memory["test"] == 370101013

    Data.clear()
    run("13")
    run("test !")
    assert Memory["test"] == 13


def test_word():
    Data.clear()

    run(
        " : fac_rec ( n -- n! ) dup 0> IF dup 1- fac_rec * ELSE drop 1 ENDIF ;"
    )
    run("6 fac_rec")
    assert Data.height() == 1
    assert Data.peek() == 720


def test_exec_fib_sample_program():
    Data.clear()

    execute_file('examples/10fibs.fs')

    assert Data.height() == 10
    assert Data.peek() == 55
    assert Data.peek(-10) == 1
