import pytest
from lexer.tokenizer import tokenize
from errors.exceptions import LexerError

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

def test_tokenize_basic_operators_and_keywords():
    code = "var x = 10; if (x > 5 && x < 20) { x += 1; }"
    tokens = [t.type for t in tokenize(code)]
    assert "VAR" in tokens
    assert "IDENTIFIER" in tokens
    assert "NUMBER" in tokens
    assert "LOGICAL_AND" in tokens
    assert "OP_PLUSEQ" in tokens

def test_tokenize_class_and_function_keywords():
    code = "class Test {} function myFunc() {} return;"
    tokens = [t.type for t in tokenize(code)]
    assert "CLASS" in tokens
    assert "FUNCTION" in tokens
    assert "RETURN" in tokens

def test_tokenize_invalid_character_raises_error():
    with pytest.raises(LexerError):
        tokenize("var x = 10 @")

def test_tokenize_operators_and_symbols():
    code = "a++; b--; c => d; obj.key;"
    tokens = [t.type for t in tokenize(code)]
    assert "OP_INCREMENT" in tokens
    assert "OP_DECREMENT" in tokens
    assert "ARROW" in tokens
    assert "DOT" in tokens
