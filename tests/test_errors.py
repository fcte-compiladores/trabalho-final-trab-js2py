import pytest
from errors.exceptions import LexerError, ParserError, TranspilerError

def test_custom_error_messages():
    err1 = LexerError(char="@", position=10, source_line="line 1")
    err2 = ParserError(expected="IDENTIFIER", found="EOF", position=5, context="Missing token")
    err3 = TranspilerError("UnknownNode", "No method implemented")
    assert "@" in str(err1)
    assert "IDENTIFIER" in str(err2)
    assert "Erro na transpilação" in str(err3)

