import pytest
from parser.parser import Parser
from interpreter.interpreter import Interpreter

def run_js(js_code):
    parser = Parser(js_code)
    ast = parser.parse_program()
    interpreter = Interpreter(ast)
    return interpreter.execute()

def test_interpret_variable():
    run_js('var x = 10;')
    assert True  # Não quebra

def test_if_else():
    code = 'var x = 5; if (x > 3) { x = 20; } else { x = 0; }'
    parser = Parser(code)
    ast = parser.parse_program()
    interpreter = Interpreter(ast)
    interpreter.execute()
    assert interpreter.environment['x'] == 20

def test_while_loop():
    code = 'var x = 0; while (x < 3) { x = x + 1; }'
    parser = Parser(code)
    ast = parser.parse_program()
    interpreter = Interpreter(ast)
    interpreter.execute()
    assert interpreter.environment['x'] == 3

def test_function_call():
    code = 'function soma(a,b){ return a+b; } soma(2,3);'
    parser = Parser(code)
    ast = parser.parse_program()
    interpreter = Interpreter(ast)
    interpreter.execute()
    assert 'soma' in interpreter.environment

def test_array_and_object():
    code = 'var arr = [1,2]; var obj = { a: 1, b: 2 };'
    run_js(code)

def test_class_and_method():
    code = '''
    class Pessoa {
        constructor(nome){ this.nome = nome; }
        falar(){ console.log(this.nome); }
    }
    var p = new Pessoa("João");
    p.falar();
    '''
    run_js(code)

def test_error_variable_not_defined():
    code = 'console.log(x);'
    with pytest.raises(NameError):
        run_js(code)
