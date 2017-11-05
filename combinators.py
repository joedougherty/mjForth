# -*- coding: utf-8 -*-


from core import Data, Words, wordify
from mjForth import consume_tokens, tokenize


def unquote():
    """ Unquote! """
    stack_rep = Data.pop().replace('[','').replace(']','')
    consume_tokens(tokenize(stack_rep))


Words['i'] = wordify(unquote)
