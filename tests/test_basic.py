"""
Testes básicos para verificar se o pytest está funcionando
"""
import pytest

def test_basic():
    """Teste básico para verificar se o pytest está funcionando"""
    assert 1 + 1 == 2

def test_string():
    """Teste com strings"""
    assert "hello" + " world" == "hello world"

def test_list():
    """Teste com listas"""
    my_list = [1, 2, 3]
    assert len(my_list) == 3
    assert 2 in my_list
