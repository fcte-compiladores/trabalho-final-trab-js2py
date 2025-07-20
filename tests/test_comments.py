import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser.parser import Parser
from translator.transpiler import Transpiler
from interpreter.interpreter import Interpreter

def test_single_line_comments():
    """Testa comentários de linha simples"""
    code = """
    // Comentário simples
    let x = 5;
    """
    parser = Parser(code)
    ast = parser.parse_program()
    
    transpiler = Transpiler(ast)
    python_code = transpiler.transpile()
    
    assert "# Comentário simples" in python_code
    assert "x = 5" in python_code

def test_multiline_comments():
    """Testa comentários multilinha"""
    code = """
    /*
        Comentário multilinha
        com várias linhas
    */
    let y = 10;
    """
    parser = Parser(code)
    ast = parser.parse_program()
    
    transpiler = Transpiler(ast)
    python_code = transpiler.transpile()
    
    assert "# Comentário multilinha" in python_code
    assert "# com várias linhas" in python_code
    assert "y = 10" in python_code

def test_inline_comments():
    """Testa comentários inline"""
    code = """
    let z = 15; // Comentário inline
    """
    parser = Parser(code)
    ast = parser.parse_program()
    
    transpiler = Transpiler(ast)
    python_code = transpiler.transpile()
    
    assert "z = 15  # Comentário inline" in python_code

def test_mixed_comments():
    """Testa mistura de tipos de comentários"""
    code = """
    // Comentário de linha
    /* Comentário multilinha */
    let a = 1; // Inline
    """
    parser = Parser(code)
    ast = parser.parse_program()
    
    transpiler = Transpiler(ast)
    python_code = transpiler.transpile()
    
    assert "# Comentário de linha" in python_code
    assert "# Comentário multilinha" in python_code
    assert "a = 1  # Inline" in python_code

def test_comment_interpretation():
    """Testa que comentários não afetam a interpretação"""
    code = """
    // Comentário
    let x = 5;
    console.log(x); // Inline comment
    """
    parser = Parser(code)
    ast = parser.parse_program() 
    interpreter = Interpreter(ast)
    interpreter.execute()

if __name__ == "__main__":
    test_single_line_comments()
    test_multiline_comments()
    test_inline_comments()
    test_mixed_comments()
    test_comment_interpretation()
    print("Todos os testes de comentários passaram!")
