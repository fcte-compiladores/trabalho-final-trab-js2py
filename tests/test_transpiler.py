from parser.parser import Parser
from translator.transpiler import Transpiler

def transpile_js(js_code):
    parser = Parser(js_code)
    ast = parser.parse_program()
    transpiler = Transpiler(ast)
    return transpiler.transpile()

def test_transpile_variable():
    code = 'var x = 10;'
    py_code = transpile_js(code)
    assert 'x = 10' in py_code

def test_transpile_if():
    code = 'if (x > 5) { console.log("maior"); } else { console.log("menor"); }'
    py_code = transpile_js(code)
    assert 'if (x > 5):' in py_code

def test_transpile_function():
    code = 'function add(a,b){ return a+b; }'
    py_code = transpile_js(code)
    assert 'def add(a, b):' in py_code

def test_transpile_class():
    code = 'class Pessoa { constructor(nome){ this.nome = nome; } falar(){ console.log(this.nome); } }'
    py_code = transpile_js(code)
    assert 'class Pessoa:' in py_code
