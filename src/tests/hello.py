from i13c.lex import tokenize

def can_tokenize():
    assert tokenize() is None
