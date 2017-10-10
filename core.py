# -*- coding: utf-8 -*-

from Stack import Stack 

from functools import wraps
import operator
import sys


Data = Stack()
Return = Stack()


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
    Data.push(int(Data.pop() / (Data.pop()*1.0)))


def mod():
    """ Custom mod. """
    a, b = Data.pop(), Data.pop()
    Data.push(operator.mod(b,a))


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


def wordify(word_as_fn):
    return {'doc': word_as_fn.__doc__, 'fn': word_as_fn}


Env =  {'exit'  : {'doc': 'Exits the session.', 'fn': sys.exit},
        '+'     : wordify(add),
        '-'     : wordify(subtract),
        '*'     : wordify(multiply),
        '/'     : wordify(divide),
        'mod'   : wordify(mod), 
        'drop'  : wordify(drop),
        'swap'  : wordify(swap),
        'dup'   : wordify(dup),
        'over'  : wordify(over),
        'rot'   : wordify(rot),
        'nip'   : wordify(nip),
        'tuck'  : wordify(tuck),
        '.'     : wordify(dot),
        '.s'    : wordify(dot_s),
        'words' : wordify(words)}

# Aliases
Env['add'] = Env['+']
Env['subtract'] = Env['-']
Env['multiply'] = Env['*']
Env['divide'] = Env['/']
