def tokenize(s):
    r = list(s)
    return [i for i in r if i != ' ']


def _consume_list(tokens):
    token = tokens.pop(0)
    if '[' == token:
        L = []
        while tokens[0] != ']':
            L.append(_consume_list(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ']' == token:
        raise SyntaxError('unexpected )')
    else:
        return token


def relistify(list_as_str):
    s = str(list_as_str).replace(',','').replace("'",'')
    s = s.replace('[','[ ').replace(']', ' ]')
    return s


def consume_list(input_list_ref):
    list_body = _consume_list(input_list_ref)
    return relistify(list_body)
