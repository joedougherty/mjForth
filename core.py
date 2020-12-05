# -*- coding: utf-8 -*-

from copy import copy
import operator
import sys


class StackUnderflowError(Exception):
    pass


class StackOverflowError(Exception):
    pass


class Stack:
    def __init__(self, height_limit=None):
        self.contents = []
        self.height_limit = height_limit

    def push(self, item):
        if self.height_limit:
            if (self.height() + 1) > self.height_limit:
                msg = "This Stack has a height_limit set to: {}".format(
                    self.height_limit
                )
                raise StackOverflowError(msg)
        self.contents.append(item)

    def pop(self, idx=None):
        try:
            if idx is None:
                return self.contents.pop()
            else:
                return self.contents.pop(idx)
        except IndexError:
            raise StackUnderflowError("Not enough items on the stack to `pop()`!")

    def peek(self, idx=-1):
        try:
            return self.contents[idx]
        except IndexError:
            raise StackUnderflowError("Not enough items on the stack to `peek()`!")

    def is_empty(self):
        return self.height() == 0

    def height(self):
        return len(self.contents)

    def clear(self):
        self.contents.clear()


TRUE = -1
FALSE = 0

Data = Stack()
Return = Stack()
Memory = dict()


def clear(Data=Data):
    """ Empty the (data/parameter) stack! """
    Data.clear()


def drop(Data=Data):
    Data.pop()


def swap(Data=Data):
    a, b = Data.pop(), Data.pop()
    Data.push(a)
    Data.push(b)


def dup(Data=Data):
    Data.push(copy(Data.peek()))


def over(Data=Data):
    copiedval = copy(Data.peek(-2))
    Data.push(copiedval)


def rot(Data=Data):
    Data.push(Data.pop(-3))


def nip(Data=Data):
    swap(Data=Data)
    drop(Data=Data)


def tuck(Data=Data):
    swap(Data=Data)
    over(Data=Data)


def add(Data=Data):
    """ This is a custom `add` implementation. """
    Data.push(Data.pop() + Data.pop())


def subtract(Data=Data):
    """ This is a custom `subtract` implementation. """
    a, b = Data.pop(), Data.pop()
    Data.push(b - a)


def multiply(Data=Data):
    """ This is a custom `multiply` implementation. """
    Data.push(Data.pop() * Data.pop())


def divide(Data=Data):
    """ This is a custom `divide` implementation. """
    a, b = Data.pop(), Data.pop()
    Data.push(int(b / (a * 1.0)))


def mod(Data=Data):
    """ Custom mod. """
    a, b = Data.pop(), Data.pop()
    Data.push(operator.mod(b, a))


def equals(Data=Data):
    """ Are the top two stack items equal? """
    if Data.pop() == Data.pop():
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def equals_zero(Data=Data):
    """ Pop the top. Does it equal 0? """
    top = Data.pop()
    if top == 0:
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def dot(Data=Data):
    """ Pop 'n print! """
    print((Data.pop()))


def dot_s(Data=Data):
    """ Print stack and stack height. """
    print(("<{}> {}".format(Data.height(), " ".join([str(i) for i in Data.contents]))))


def words():
    """ List the known words. """
    word_list = ""
    for word in Words:
        word_list += word + " "
    print(word_list)


def greaterthan(Data=Data):
    """ > ? """
    a, b = Data.pop(), Data.pop()
    if b > a:
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def lessthan(Data=Data):
    """ < ? """
    a, b = Data.pop(), Data.pop()
    if b < a:
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def minusone(Data=Data):
    """ Subtract 1 from the top val of the stack. """
    Data.push(Data.pop() - 1)


def plusone(Data=Data):
    """ Add 1 to the top val of the stack. """
    Data.push(Data.pop() + 1)


def greater_than_zero(Data=Data):
    """ Is top val greater than zero? """
    if Data.pop() > 0:
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def showmem(Memory=Memory):
    if Memory == dict():
        print("No global variables defined!")
    else:
        for k, v in list(Memory.items()):
            print(("{}: {}".format(k, v)))


def negate(Data=Data):
    """ n -- -n """
    Data.push(Data.pop() * -1)


def _abs(Data=Data):
    """  n -- |n| """
    Data.push(abs(Data.pop()))


def _min(Data=Data):
    """ n1 n2 -- n-min """
    Data.push(min([Data.pop(), Data.pop()]))


def _max(Data=Data):
    """ n1 n2 -- n-max """
    Data.push(max([Data.pop(), Data.pop()]))


def wordify(word_as_fn):
    return {"doc": word_as_fn.__doc__, "fn": word_as_fn}


Words = {
    "exit": {"doc": "Exits the session.", "fn": sys.exit},
    "+": wordify(add),
    "-": wordify(subtract),
    "*": wordify(multiply),
    "/": wordify(divide),
    "mod": wordify(mod),
    "drop": wordify(drop),
    "swap": wordify(swap),
    "dup": wordify(dup),
    "over": wordify(over),
    "rot": wordify(rot),
    "nip": wordify(nip),
    "tuck": wordify(tuck),
    ".": wordify(dot),
    ".s": wordify(dot_s),
    "words": wordify(words),
    "clear": wordify(clear),
    "0=": wordify(equals_zero),
    "0>": wordify(greater_than_zero),
    "=": wordify(equals),
    ">": wordify(greaterthan),
    "<": wordify(lessthan),
    "1-": wordify(minusone),
    "1+": wordify(plusone),
    "showmem": wordify(showmem),
    "negate": wordify(negate),
    "abs": wordify(_abs),
    "min": wordify(_min),
    "max": wordify(_max),
}

# Aliases
Words["add"] = Words["+"]
Words["subtract"] = Words["-"]
Words["multiply"] = Words["*"]
Words["divide"] = Words["/"]
Words["quit"] = Words["exit"]
