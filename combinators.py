# -*- coding: utf-8 -*-


from core import Data, Words, wordify
from mjForth import consume_tokens, tokenize


def _strip_quotes(quoted_str, outer_only=True):
    if not isinstance(quoted_str, str) and not isinstance(quoted_str, bytes):
        return quoted_str

    if outer_only:
        if quoted_str.startswith('['):
            quoted_str = quoted_str[1:]
        if quoted_str.endswith(']'):
            quoted_str = quoted_str[:-1]
        return quoted_str.strip()
    else:
        return quoted_str.replace(']', '').replace('[', '')

"""
To some extent, the chosen combinators reflect 
those discussed here: http://tunes.org/~iepos/joy.html
"""
def unquote():
    """ Unquote! """
    consume_tokens(tokenize(_strip_quotes(Data.pop())))


def concat():
    """ [ B ] [ A ] concat => [ B A ] """
    list1, list2 = Data.pop(), Data.pop()
    combined_list = '[ {} {} ]'.format(_strip_quotes(list2),  _strip_quotes(list1))
    Data.push(combined_list)


def cons():
    """ [ B ] [ A ] cons => [ [ B ] A ] """
    A, B = Data.pop(), Data.pop()
    list_rep = '[ {} {} ]'.format(B, _strip_quotes(A)).replace('  ', ' ')
    Data.push(list_rep)


def dip():
    """ 
    [ B ] [ A ] => A [ B ]
    Pop two quoted programs off the stack [A] and [B]. 
    Execute A, put [B] back on the stack. 
    """
    A, B = Data.pop(), Data.pop()
    consume_tokens(tokenize(_strip_quotes(A)))
    Data.push(B)


def unit():
    """ [ A ] => [ [ A ] ] """
    Data.push('[ {} ]'.format(Data.pop()))


def t():
    """ [ B ] [ A ] => [ A ] B """
    A, B = Data.pop(), Data.pop()
    Data.push(A)
    consume_tokens(tokenize(_strip_quotes(B)))


Words['i']      = wordify(unquote)
Words['concat'] = wordify(concat)
Words['cons']   = wordify(cons)
Words['dip']    = wordify(dip) 
Words['unit']   = wordify(unit)
Words['t']      = wordify(t)
