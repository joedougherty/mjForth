# -*- coding: utf-8 -*-


from core import Data, Words, wordify
from mjForth import consume_tokens, tokenize


def _strip_quotes(quoted_str, outer_only=True):
    if outer_only:
        if quoted_str.startswith('['):
            quoted_str = quoted_str[1:]
        if quoted_str.endswith(']'):
            quoted_str = quoted_str[:-1]
        return quoted_str.strip()
    else:
        return quoted_str.replace(']', '').replace('[', '')


def unquote():
    """ Unquote! """
    consume_tokens(tokenize(_strip_quotes(Data.pop())))


def concat():
    """ Concat two quoted lists. """
    list1, list2 = Data.pop(), Data.pop()
    combined_list = '[ {} {} ]'.format(_strip_quotes(list2),  _strip_quotes(list1))
    Data.push(combined_list)


Words['i'] = wordify(unquote)
Words['concat'] = wordify(concat)
