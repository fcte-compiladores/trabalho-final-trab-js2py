import pytest
from parser.parser import Parser
from translator.transpiler import Transpiler
from errors.exceptions import TranspilerError

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

def transpile(js_code):
    parser = Parser(js_code)
    ast = parser.parse_program()
    return Transpiler(ast).transpile()

def test_binary_and_string_concat_transpile():
    code = "if (x && y) { var z = 'a' + 1; }"
    py_code = transpile(code)
    assert "and" in py_code
    assert "str(" in py_code

def test_for_loops_and_methods_transpile():
    code = '''
    for (var i = 0; i < 3; i++) { console.log(i); }
    for (var x of arr) { console.log(x); }
    var s = 'abc'; s.charAt(0); s.substr(1,2);
    '''
    py_code = transpile(code)
    assert "while" in py_code
    assert "for x in" in py_code
    assert "[0]" in py_code
    assert "s[1:1+2]" in py_code

def test_transpiler_error_unknown_node():
    class FakeNode: pass
    with pytest.raises(TranspilerError):
        Transpiler(None).generic_visit(FakeNode())

def transpile(js):
    return Transpiler(Parser(js).parse_program()).transpile()

def test_transpile_class_with_constructor_and_method():
    code = """
    class Pessoa {
        constructor(nome) { this.nome = nome; }
        falar() { console.log(this.nome); }
    }
    """
    py_code = transpile(code)
    assert "def __init__(self, nome)" in py_code
    assert "def falar(self)" in py_code

def test_transpile_update_expression():
    code = "i++; arr.length--; obj.count++;"
    py_code = transpile(code)
    assert "+ 1" in py_code or "pop()" in py_code

def test_transpile_math_and_string_methods():
    code = "Math.sqrt(4); var s = 'hi'; s.toUpperCase(); s.toFixed(2);"
    py_code = transpile(code)
    assert "math.sqrt" in py_code
    assert ".upper()" in py_code
    assert "f\"{" in py_code 

def transpile(js_code):
    return Transpiler(Parser(js_code).parse_program()).transpile()

def test_transpile_string_and_array_methods():
    code = '''
    var s = "hi";
    s.toUpperCase();
    s.toLowerCase();
    s.substr(1,2);
    var arr = [1];
    arr.push(2);
    arr.pop();
    '''
    py_code = transpile(code)
    assert ".upper()" in py_code
    assert ".lower()" in py_code
    assert ".append(" in py_code
    assert ".pop()" in py_code

def test_transpile_math_methods():
    code = '''
    Math.sqrt(4);
    Math.floor(3.7);
    Math.ceil(1.2);
    Math.pow(2,3);
    Math.max(1,2);
    Math.min(1,2);
    '''
    py_code = transpile(code)
    assert "math.sqrt" in py_code
    assert "math.floor" in py_code
    assert "math.ceil" in py_code
    assert "pow(" in py_code
    assert "max(" in py_code
    assert "min(" in py_code

def test_transpile_class_with_methods():
    code = '''
    class Car {
        constructor(name){ this.name = name; }
        drive(){ console.log(this.name); }
        stop(){ console.log("Stopped"); }
    }
    '''
    py_code = transpile(code)
    assert "class Car:" in py_code
    assert "def __init__(self, name)" in py_code
    assert "def drive(self)" in py_code
    assert "def stop(self)" in py_code
