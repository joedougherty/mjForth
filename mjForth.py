#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from core import Env as Words
from core import Data, Return

from copy import copy, deepcopy
from itertools import takewhile
import os
import readline
import sys

__version__ = '0.0.2'


def welcome():
    msg = """mjForth {}, Copyright (C) 2017 Joe Dougherty.""".format(__version__)
    msg += """\nType `exit` to quit.\n"""
    print(msg)


def takewhile_and_pop(match_token, list_of_tokens):
    """
    Remove tokens from the list_of_tokens until the match_token
    is encountered.

    Return the matched tokens as a new list. Remove the applicable
    tokens from list_of_tokens.
    """

    if match_token not in list_of_tokens:
        print('Expected to encounter \'{}\', but did not see it in list_of_tokens!'.format(match_token))
        return False

    tw = [i for i in takewhile(lambda t: t != match_token, list_of_tokens)]
    for found_item in tw:
        list_of_tokens.pop(0)
    list_of_tokens.pop(0) # Remove matching character
    return tw


def must_be_defined(word):
    safe_words = ('?DO', 'i', 'LOOP', '', ' ')
    return (word not in Words
        and not word.isnumeric()
        and word not in safe_words)


def define_word(input_list_ref):
    """
    Extract the name, paren comment, and body for the word being defined.

    This function will be called if the preceding token is ':'

    If the remaining input string can't be parsed correctly,
    input_list_ref will be .clear()'ed and we'll return False.

    If the input string *can* be parsed, the newly defined
    word will added to the globally-accessible Words dict.
    """
    name = input_list_ref.pop(0)
    if input_list_ref[0] == '(':
        input_list_ref.pop(0) # Pop (
        comment = takewhile_and_pop(')', input_list_ref)
    else:
        print("Name must be followed by paren docs! Was trying to define: '{}'".format(name))
        input_list_ref.clear()
        return False
    body = takewhile_and_pop(';', input_list_ref)

    for word in body:
        if must_be_defined(word):
            print("You must define `{}` before invoking it!!!".format(word))
            input_list_ref.clear()
            return False

    if name in Words:
        print("'{}' was redefined.".format(name))

    Words[name] = {'doc': comment, 'fn': body}


def show_definition(word):
    if word not in Words:
        print("{} has not been defined!".format(word))
        return False

    if isinstance(Words[word]['doc'], list):
        print('({})'.format(' '.join(Words[word]['doc'])))
    if isinstance(Words[word]['doc'], str):
        print('({})'.format(Words[word]['doc']))
    if callable(Words[word]['fn']):
        print('  ' + Words[word]['fn'].__name__)
    if isinstance(Words[word]['fn'], list):
        print('  ' + ' '.join([str(i) for i in Words[word]['fn']]))


def call_word(term, input_list_ref):
    if isinstance(Words[term]['fn'], list):
        fn_list = copy(Words[term]['fn'])
        while fn_list:
            token = fn_list.pop(0)
            handle_term(token, fn_list)
    elif callable(Words[term]['fn']):
        try:
            Words[term]['fn']()
        except IndexError:
            print("Empty stack!!!")
    else:
        print("I don't know what to do with `{}` !!!".format(term))


def run_loop(fn_body_as_word_list):
    _from, _to = Data.pop(), Data.pop()
    for i in range(_from, _to):
        for item in fn_body_as_word_list:
            if item == 'i':
                item = str(i)
            handle_term(item, fn_body_as_word_list)


def handle_term(term, input_list_ref):
    if term == '':
        return True
    if term.isnumeric():
        Data.push(int(term))
    elif term == ':': # Function definition
        define_word(input_list_ref)
    elif term == '?DO':
        # Execute DO LOOP
        doloop_body = takewhile_and_pop('LOOP', input_list_ref)
        run_loop(doloop_body)
    elif term in Words: # Function call
        call_word(term, input_list_ref)
    elif term == 'see': # Function documentation
        show_definition(input_list_ref.pop())
    else:
        print("I don't know what to do with `{}` !!!".format(term))


def clean_input_line(input_line):
    return input_line.strip().  \
           replace('(', '( ').  \
           replace(')', ' )').  \
           replace(';', ' ; '). \
           split(' ')


def main():
    welcome()

    while True:
        try:
            input_list = clean_input_line(input('mjF> '))
            while input_list:
                term = input_list.pop(0)
                handle_term(term, input_list)
        except KeyboardInterrupt:
            print('')
        except EOFError:
            print('')
            sys.exit()


def execute_file(abs_path_to_file):
    with open(abs_path_to_file, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    for line in lines:
        input_list = clean_input_line(line)
        while input_list:
            term = input_list.pop(0)
            handle_term(term, input_list)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] and os.path.exists(sys.argv[1]):
        execute_file(sys.argv[1])
    else:
        main()

