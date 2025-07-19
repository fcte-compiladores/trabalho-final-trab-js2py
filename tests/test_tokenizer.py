import pytest
from lexer.tokenizer import tokenize

def test_tokenize_basic():
    code = 'var x = 10;'
    tokens = tokenize(code)
    types = [t.type for t in tokens]
    assert types == ['VAR', 'IDENTIFIER', 'OP_ASSIGN', 'NUMBER', 'SEMICOLON']

def test_tokenize_string():
    code = 'var msg = "hello";'
    tokens = tokenize(code)
    assert any(t.type == 'STRING' for t in tokens)

def test_tokenize_comment():
    code = '// this is a comment'
    tokens = tokenize(code)
    assert tokens[0].type == 'COMMENT'
