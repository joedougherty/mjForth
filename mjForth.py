#!/usr/bin/env python3

# -*- coding: utf-8 -*-

###-----------------------------------------------------------------###
#
#   Table of Contents
#   =================
#
#   Section 1: imports, custom classes/exceptions, reserved words
#   Section 2: definining words, calling words
#   Section 3: for loops, while loops, if/endif, if/else/endif
#   Section 4: variable declaration, setting, retrieval 
#   Section 5: token parsing and handling 
#   Section 6: run the main() loop, tokenize() -> consume_tokens()
#
###-----------------------------------------------------------------###


###-----------------------------------------------------------------###
#   Section 1: imports, custom classes/exceptions, reserved words
###-----------------------------------------------------------------###
from core import Data, TRUE, FALSE, Memory, Words, Word

from copy import copy
import os
import readline
import sys

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter


__version__ = "0.0.5"


class RunTimeError(Exception):
    pass


class InputStream:
    ''' A thin wrapper around a token list. '''
    def __init__(self, input_list):
        self._contents = input_list

    def has_tokens(self):
        return len(self._contents) >= 1

    def clear(self):
        self._contents.clear()

    def take(self, n):
        agg = []
        for i in range(0,n):
            agg.append(next(self))
        return agg

    def __iter__(self):
        return iter(self._contents)

    def __next__(self):
        try:
            return self._contents.pop(0)
        except IndexError:
            raise RunTimeError("Empty stack")

    def __contains__(self, value):
        return value in self._contents


RESERVED = (
    "?DO",
    "i",
    "LOOP",
    "",
    " ",
    "IF",
    "ELSE",
    "ENDIF",
    "variable",
    "true",
    "false",
    "BEGIN",
    "WHILE",
    "REPEAT",
    "!",
    "@",
    "]",
    "[",
)


def take_tokens(from_token, match_token, input_stream):
    if match_token not in input_stream:
        raise SyntaxError(
            f"""Expected to encounter '{match_token}' in expression: \n"""
            f"""{from_token} {" ".join(list_of_tokens)}"""
        )

    if isinstance(input_stream, InputStream):
        input_list = input_stream._contents
    elif isinstance(input_stream, list):
        input_list = input_stream

    agg = []
    while input_list:
        token = input_list.pop(0)
        if token == match_token:
            break
        else:
            agg.append(token)

    return agg


###-----------------------------------------------------------------###
#   Section 2: Words
###-----------------------------------------------------------------###
def must_be_defined(word):
    return (
        word not in Words.keys()
        and word not in Memory.keys()
        and word not in RESERVED
        and not is_a_literal(word)[0]
    )


def define_word(input_stream):
    ''' 
    Extract the name, paren comment, and body for the word. 
    Add the newly compiled word to Words.
    '''
    name, open_paren = input_stream.take(2)

    if open_paren != "(":
        input_stream.clear()
        raise SyntaxError("definitions need a stack comment in ( )!")

    comment = take_tokens("(", ")", input_stream)
    body = take_tokens(":", ";", input_stream)

    for word in body:
        if must_be_defined(word) and word != name:
            input_stream.clear()
            raise RunTimeError(
                f"""You must define `{word}` before invoking it!"""
            )

    redefined = name in Words.keys()

    Words[name] = Word(comment, body)

    if redefined:
        print(f"""`{name}` was redefined.""")


def show_definition(word):
    if word not in Words.keys():
        raise RunTimeError(f"""`{word}` has not been defined!""")

    doc, definition = Words[word].doc, Words[word].definition

    if isinstance(doc, list):
        doc = " ".join([str(i) for i in doc])

    if callable(definition):
        print(f"""  {definition.__name__} [built-in]""")
    elif isinstance(definition, list):
        print(f""": {word}\n  ( {doc} )\n  {" ".join(definition)} ; """)


def call_word(word):
    if word not in Words.keys():
        raise RunTimeError(f"""`{word}` has not been defined!""")

    fn = Words[word].definition

    if callable(fn):
        fn()
    elif isinstance(fn, list):
        consume_tokens(copy(fn))
    else:
        raise RunTimeError(
            f'''{fn} was neither callable or list of words!'''
        )

###-----------------------------------------------------------------###
#   Section 3: for loops, while loops, conditionals 
###-----------------------------------------------------------------###
def _resolve_iterator(i, fn_body_as_word_list):
    ''' Replace 'i' with a string version of the current iterator. '''
    for idx, item in enumerate(fn_body_as_word_list):
        if item == "i":
            fn_body_as_word_list[idx] = str(i)

    return fn_body_as_word_list


def run_doloop(word_list):
    _from, _to = Data.pop(), Data.pop()

    for i in range(_from, _to):
        input_list = _resolve_iterator(i, copy(word_list))
        consume_tokens(input_list)


# https://www.complang.tuwien.ac.at/forth/gforth/Docs-html/Simple-Loops.html#Simple-Loops
def run_whileloop(while_loop_body):
    code1_and_flag = take_tokens("WHILE", "REPEAT", while_loop_body)
    code2 = while_loop_body

    flag_value = TRUE
    while flag_value == TRUE:
        consume_tokens(copy(code1_and_flag))
        if Data.pop() == TRUE:
            consume_tokens(copy(code2))
        else:
            flag_value = FALSE


def run_conditional(input_stream):
    cond_body = take_tokens("IF", "ENDIF", input_stream)
    if "ELSE" not in cond_body:
        # This is a simple statement. No ELSE to contend with.
        if Data.pop() == TRUE:
            consume_tokens(cond_body)
    else:
        iftrue = take_tokens("IF", "ELSE", cond_body)
        otherwise = cond_body
        if Data.pop() == TRUE:
            consume_tokens(iftrue)
        else:
            consume_tokens(otherwise)

###-----------------------------------------------------------------###
#   Section 4: variable declaration, setting, retrieval 
###-----------------------------------------------------------------###
def declare_variable(varname):
    if varname in Memory.keys():
        raise RunTimeError(f"""{varname} has already been declared.""")

    Memory[varname] = None


def set_or_get_variable(token, input_stream):
    next_token = next(input_stream)

    if next_token not in ("!", "@"):
        input_stream.clear()
        raise SyntaxError(
            f"""Was trying to get or set '{token}', but missing ! or @"""
        )

    if next_token == "!":
        Memory[token] = Data.pop()
    else:  # next_token == "@"
        Data.push(Memory[token])

###-----------------------------------------------------------------###
#   Section 5: token parsing and handling 
###-----------------------------------------------------------------###
def is_a_literal(token):
    if token == "true":
        return (True, TRUE)
    if token == "false":
        return (True, FALSE)

    try:
        return (True, int(token))
    except ValueError:
        try:
            return (True, float(token))
        except ValueError:
            return (False, token)
    return (False, token)


def handle_token(token, input_stream):
    token_is_literal, parsed = is_a_literal(token)

    if token_is_literal:
        # Push literals on to the Data stack
        Data.push(parsed)
    elif token in Words.keys():
        # token is a Word -- call it!
        call_word(token)
    elif token in Memory.keys():
        # Get a variable definition or redefine existing variable
        set_or_get_variable(token, input_stream)
    elif token == "see":
        # Show a Word's definition
        show_definition(next(input_stream))
    elif token == ":":
        # Define a new Word
        define_word(input_stream)
    elif token == "?DO":
        # Execute DO loop
        doloop_body = take_tokens("?DO", "LOOP", input_stream)
        run_doloop(doloop_body)
    elif token == "BEGIN":
        # Execute WHILE loop
        whileloop_body = take_tokens("BEGIN", "WHILE", input_stream)
        run_whileloop(whileloop_body)
    elif token == "IF":
        # Handle Conditionals
        run_conditional(input_stream)
    elif token == "variable":
        # Declare the existence of a new variable in Memory
        declare_variable(next(input_stream))
    else:
        raise SyntaxError(
            f"""I don't know what to do with `{token}` !!!"""
        )

###-----------------------------------------------------------------###
#   Section 6: run the main() loop, tokenize() -> consume_tokens()
###-----------------------------------------------------------------###
def tokenize(input_line):
    input_line = (
        input_line.strip()
        .replace("(", "( ")
        .replace(")", " )")
        .replace(";", " ; ")
        .split(" ")
    )

    return [token for token in input_line if token != ""]


def consume_tokens(input_list):
    if isinstance(input_list, InputStream):
        input_stream = input_list
    else:
        input_stream = InputStream(input_list)

    while input_stream.has_tokens():
        token = next(input_stream)
        handle_token(token, input_stream)


def main():
    print(
        f"""mjForth {__version__}, Copyright (C) 2018-2020 Joe Dougherty."""
    )

    while True:
        try:
            consume_tokens(
                tokenize(
                    prompt(
                        "mjF> ",
                        history=FileHistory(".mjForth_history"),
                        completer=WordCompleter(
                            list(Words.keys()) + ["see", "variable"]
                        ),
                    )
                )
            )
            print(f"""ok <{Data.height()}>""")
        except KeyboardInterrupt:
            print("")
        except (SyntaxError, RunTimeError) as e:
            print(e)
        except EOFError:
            print("")
            sys.exit(0)


def run(lines):
    if isinstance(lines, str):
        lines = [lines]

    for line in lines:
        consume_tokens(tokenize(line))


def execute_file(abs_path_to_file):
    with open(abs_path_to_file, "r") as f:
        lines = [l.strip() for l in f.readlines()]

    run(lines)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        filename = sys.argv[1]
        if os.path.exists(filename):
            execute_file(filename)
        else:
            print(f"""{filename} does not exist!""")
            sys.exit(2)
    main()
