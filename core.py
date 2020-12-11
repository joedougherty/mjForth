# -*- coding: utf-8 -*-

from collections import namedtuple
from copy import copy
import operator
import sys


from IPython import embed


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

        
Word = namedtuple('Word', ['doc', 'definition'])


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
    print(" ".join([word for word in Words]))


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


Words = {
    "exit": Word("Exits the session.", sys.exit),
    "+": Word(add.__doc__, add),
    "-": Word(subtract.__doc__, subtract),
    "*": Word(multiply.__doc__, multiply),
    "/": Word(divide.__doc__, divide),
    "mod": Word(mod.__doc__, mod),
    "drop": Word(drop.__doc__, drop),
    "swap": Word(swap.__doc__, swap),
    "dup": Word(dup.__doc__, dup),
    "over": Word(over.__doc__, over),
    "rot": Word(rot.__doc__, rot),
    "nip": Word(nip.__doc__, nip),
    "tuck": Word(tuck.__doc__, tuck),
    ".": Word(dot.__doc__, dot),
    ".s": Word(dot_s.__doc__, dot_s),
    "words": Word(words.__doc__, words),
    "clear": Word(clear.__doc__, clear),
    "0=": Word(equals_zero.__doc__, equals_zero),
    "0>": Word(greater_than_zero.__doc__, greater_than_zero),
    "=": Word(equals.__doc__, equals),
    ">": Word(greaterthan.__doc__, greaterthan),
    "<": Word(lessthan.__doc__, lessthan),
    "1-": Word(minusone.__doc__, minusone),
    "1+": Word(plusone.__doc__, plusone),
    "showmem": Word(showmem.__doc__, showmem),
    "negate": Word(negate.__doc__, negate),
    "abs": Word(_abs.__doc__, _abs),
    "min": Word(_min.__doc__, _min),
    "max": Word(_max.__doc__, _max),
    "^esc": Word("IPython escape hatch.", embed),
}

# Aliases
Words["add"] = Words["+"]
Words["subtract"] = Words["-"]
Words["multiply"] = Words["*"]
Words["divide"] = Words["/"]
Words["quit"] = Words["exit"]
