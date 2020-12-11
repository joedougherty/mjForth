#!/usr/bin/env python3

# -*- coding: utf-8 -*-


from core import Data, TRUE, FALSE, Memory, Words, Word

from copy import copy
from itertools import takewhile
import os
import readline
import sys

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter


__version__ = "0.0.5"


class RunTimeError(Exception):
    pass


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


def takewhile_and_pop(from_token, match_token, list_of_tokens):
    """
    Remove tokens from the list_of_tokens until the match_token
    is encountered.

    Return the matched tokens as a new list. Remove the applicable
    tokens from list_of_tokens.
    """
    if match_token not in list_of_tokens:
        raise SyntaxError(
            f'''Expected to encounter '{match_token}' in expression: \n'''
            f'''{from_token} {" ".join(list_of_tokens)}'''
        )

    tw = [i for i in takewhile(lambda t: t != match_token, list_of_tokens)]

    for found_item in tw:
        list_of_tokens.pop(0)
    list_of_tokens.pop(0)  # Remove matching character
    return tw

###---###

def must_be_defined(word):
    return (
        word not in Words
        and word not in Memory
        and word not in RESERVED
        and not is_a_literal(word)[0]
    )


def define_word(input_list_ref):
    """
    Extract the name, paren comment, and body for the word being defined.

    This function will be called if the preceding token is ':'

    If the input string can be parsed:
        * the newly defined word will added to Words

    If the remaining input string can't be parsed:
        * input_list_ref will be .clear()'ed
        * raise SyntaxError
    """
    name = input_list_ref.pop(0)
    next_token = input_list_ref.pop(0)  # Pop (

    if next_token != "(":
        input_list.clear()
        raise SyntaxError("definitions need a stack comment in ( )!")

    comment = takewhile_and_pop("(", ")", input_list_ref)
    body = takewhile_and_pop(":", ";", input_list_ref)

    for word in body:
        if must_be_defined(word) and word != name:
            input_list_ref.clear()
            raise RunTimeError(f"""You must define `{word}` before invoking it!""")

    if name in Words.keys():
        print(f"""`{name}` was redefined.""")

    Words[name] = Word(comment, body) 


def show_definition(word):
    doc, definition = Words[word].doc, Words[word].definition

    if isinstance(doc, list):
        doc = " ".join([str(i) for i in doc])

    if callable(definition):
        print(f"""  {definition.__name__} [built-in]""")
    elif isinstance(definition, list):
        joined_def = " ".join(definition)
        print(f""": {word}\n  ( {doc} )\n  {joined_def} ; """)
    else:
        print(f"""{word} has not been defined!""")


def call_word(word):
    fn = Words[word].definition

    if callable(fn):
        fn()
    elif isinstance(fn, list):
        consume_tokens(copy(fn))
    else:
        raise RunTimeError(f"""{word} is neither a function nor a list of words!""")

###---###

def resolve_iterator(i, fn_body_as_word_list):
    """
    Given an input list as fn_body_as_word_list,
    replace instances of 'i' with a string version
    of the current iterator.
    """
    for idx, item in enumerate(fn_body_as_word_list):
        if item == "i":
            fn_body_as_word_list[idx] = str(i)

    return fn_body_as_word_list


def run_doloop(word_list):
    _from, _to = Data.pop(), Data.pop()

    for i in range(_from, _to):
        input_list = resolve_iterator(i, copy(word_list))
        consume_tokens(input_list)


# https://www.complang.tuwien.ac.at/forth/gforth/Docs-html/Simple-Loops.html#Simple-Loops
def run_whileloop(while_loop_body):
    code1_and_flag = takewhile_and_pop("WHILE", "REPEAT", while_loop_body)
    code2 = while_loop_body

    flag_value = TRUE
    while flag_value == TRUE:
        consume_tokens(copy(code1_and_flag))
        if Data.pop() == TRUE:
            consume_tokens(copy(code2))
        else:
            flag_value = FALSE


def parse_conditional(input_list_ref):
    cond_body = takewhile_and_pop("IF", "ENDIF", input_list_ref)
    if "ELSE" not in cond_body:
        # This is a simple statement. No ELSE to contend with.
        if Data.pop() == TRUE:
            consume_tokens(cond_body)
    else:
        iftrue = takewhile_and_pop("IF", "ELSE", cond_body)
        otherwise = cond_body
        if Data.pop() == TRUE:
            consume_tokens(iftrue)
        else:
            consume_tokens(otherwise)

###---###

def declare_variable(varname):
    if varname in Memory:
        raise RunTimeError(f"""{varname} has already been declared.""")

    Memory[varname] = None


def set_or_get_variable(token, input_list_ref):
    next_token = input_list_ref.pop(0)

    if next_token not in ("!", "@"):
        input_list_ref.clear()
        raise SyntaxError(f'''Was trying to get or set variable '{token}', but line missing ! or @''')

    if next_token == "!":
        Memory[token] = Data.pop()
    else: # next_token == "@"
        Data.push(Memory[token])

###---###

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


###---###

def handle_token(token, input_list_ref):
    token_is_literal, parsed = is_a_literal(token)

    if token_is_literal:  
        # Push literals on to the Data stack
        Data.push(parsed)
    elif token in Words.keys():  
        # token is a Word -- call it!
        call_word(token)
    elif token in Memory:  
        # Get a variable definition, or redefine existing variable
        set_or_get_variable(token, input_list_ref)
    elif token == "see":  
        # Show a Word's definition
        show_definition(input_list_ref.pop(0))
    elif token == ":":  
        # Define a new Word
        define_word(input_list_ref)
    elif token == "?DO":  
        # Execute DO loop
        doloop_body = takewhile_and_pop("?DO", "LOOP", input_list_ref)
        run_doloop(doloop_body)
    elif token == "BEGIN":  
        # Execute WHILE loop
        whileloop_body = takewhile_and_pop("BEGIN", "WHILE", input_list_ref)
        run_whileloop(whileloop_body)
    elif token == "IF":  
        # Handle Conditionals
        parse_conditional(input_list_ref)
    elif token == "variable":  
        # Declare the existence of a new variable in Memory
        declare_variable(input_list_ref.pop(0))
    else:
        raise SyntaxError(f"""I don't know what to do with `{token}` !!!""")

###---###

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
    while input_list:
        token = input_list.pop(0)
        handle_token(token, input_list)


def read_dictionary():
    return WordCompleter(list(Words.keys()) + ["see", "variable"])


def main():
    print(f"""mjForth {__version__}, Copyright (C) 2018-2020 Joe Dougherty.""")

    history = InMemoryHistory()

    while True:
        try:
            consume_tokens(
                tokenize(prompt("mjF> ", history=history, completer=read_dictionary()))
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
