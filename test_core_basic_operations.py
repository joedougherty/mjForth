# -*- coding: utf-8 -*-

import pytest


from core import *


def test_clear():
    Data = Stack()
    clear()
    assert(Data.is_empty() == True)
