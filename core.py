# -*- coding: utf-8 -*-

from Stack import Stack

from copy import copy
import operator
import sys

TRUE = -1
FALSE = 0

Data = Stack()
Return = Stack()
Memory = dict()

def clear():
    Data.contents.clear()


def drop():
    Data.pop()


def swap():
    a, b = Data.pop(), Data.pop()
    Data.push(a)
    Data.push(b)


def dup():
    topcopy = Data.peek()
    Data.push(topcopy)


def over():
    copiedval = copy(Data.contents[-2])
    Data.push(copiedval)


def rot():
    Data.push(Data.contents.pop(0))


def nip():
    swap()
    drop()


def tuck():
    swap()
    over()


def add():
    """ This is a custom `add` implementation. """
    Data.push(Data.pop() + Data.pop())


def subtract():
    """ This is a custom `subtract` implementation. """
    a, b = Data.pop(), Data.pop()
    Data.push(b - a)


def multiply():
    """ This is a custom `multiply` implementation. """
    Data.push(Data.pop() * Data.pop())


def divide():
    """ This is a custom `divide` implementation. """
    a, b = Data.pop(), Data.pop()
    Data.push(int(b / (a*1.0)))


def mod():
    """ Custom mod. """
    a, b = Data.pop(), Data.pop()
    Data.push(operator.mod(b,a))


def equals():
    """ Are the top two stack items equal? """
    if Data.pop() == Data.pop():
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def equals_zero():
    """ Pop the top. Does it equal 0? """
    top = Data.pop()
    if top == 0:
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def dot():
    """ Pop 'n print! """
    print(Data.pop())


def dot_s():
    """ Print stack and stack height. """
    print("<{}> {}".format(Data.height(), ' '.join([str(i) for i in Data.contents])))


def words():
    """ List the known words. """
    word_list = ''
    for word in Env:
        word_list += word + ' '
    print(word_list)


def greaterthan():
    """ > ? """
    a, b = Data.pop(), Data.pop()
    if b > a:
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def lessthan():
    """ < ? """
    a, b = Data.pop(), Data.pop()
    if b < a:
        Data.push(TRUE)
    else:
        Data.push(FALSE)


def minusone():
    """ Subtract 1 from the top val of the stack. """
    Data.push(Data.pop() - 1)


def plusone():
    """ Add 1 to the top val of the stack. """
    Data.push(Data.pop() + 1)


def showmem():
    if Memory == dict():
        print('No global variables defined!')
    else:
        for k, v in Memory.items():
            print('{}: {}'.format(k, v))


def wordify(word_as_fn):
    return {'doc': word_as_fn.__doc__, 'fn': word_as_fn}


Env =  {'exit'      : {'doc': 'Exits the session.', 'fn': sys.exit},
        '+'         : wordify(add),
        '-'         : wordify(subtract),
        '*'         : wordify(multiply),
        '/'         : wordify(divide),
        'mod'       : wordify(mod),
        'drop'      : wordify(drop),
        'swap'      : wordify(swap),
        'dup'       : wordify(dup),
        'over'      : wordify(over),
        'rot'       : wordify(rot),
        'nip'       : wordify(nip),
        'tuck'      : wordify(tuck),
        '.'         : wordify(dot),
        '.s'        : wordify(dot_s),
        'words'     : wordify(words),
        'clear'     : wordify(clear),
        '0='        : wordify(equals_zero),
        '='         : wordify(equals),
        '>'         : wordify(greaterthan),
        '<'         : wordify(lessthan),
        '1-'        : wordify(minusone),
        '1+'        : wordify(plusone),
        'showmem'   : wordify(showmem)}

# Aliases
Env['add'] = Env['+']
Env['subtract'] = Env['-']
Env['multiply'] = Env['*']
Env['divide'] = Env['/']
