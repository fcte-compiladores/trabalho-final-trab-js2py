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
    assert True  

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

import pytest
from parser.parser import Parser
from interpreter.interpreter import Interpreter

def run(js_code):
    parser = Parser(js_code)
    ast = parser.parse_program()
    return Interpreter(ast).execute()

def test_arithmetic_and_logic_operations():
    code = "var x = (1 + 2) * 3; var y = (x > 5) && true; console.log(y);"
    run(code)

def test_increment_and_update_expression():
    code = "var i = 0; i++; i--; console.log(i);"
    run(code)

def test_string_and_array_methods():
    code = '''
    var s = "Hello";
    console.log(s.toUpperCase());
    var arr = [1];
    arr.push(2);
    arr.pop();
    '''
    run(code)

def test_math_functions():
    code = "console.log(Math.floor(3.7)); console.log(Math.sqrt(9)); console.log(Math.max(1,2,3));"
    run(code)

def test_this_context_and_error():
    code = "function f(){ this.nome = 'Ana'; } f();"

def run(js):
    parser = Parser(js)
    ast = parser.parse_program()
    return Interpreter(ast)

def test_unary_operations():
    code = "var a = -5; var b = +10; var c = !false;"
    interpreter = run(code)
    interpreter.execute()
    assert interpreter.environment["a"] == -5
    assert interpreter.environment["b"] == 10
    assert interpreter.environment["c"] is True

def test_update_expression_on_array_length():
    code = "var arr = [1,2]; arr.length++;"
    interpreter = run(code)
    interpreter.execute()
    assert len(interpreter.environment["arr"]) == 3

def test_invalid_method_call():
    code = "var obj = {}; obj.nonExistent();"
    interpreter = run(code)
    with pytest.raises(TypeError):
        interpreter.execute()

def test_new_expression_creates_instance():
    code = "class Pessoa { constructor(nome) { this.nome = nome; } } var p = new Pessoa('Ana');"
    interpreter = run(code)
    interpreter.execute()
    assert interpreter.environment["p"]["type"] == "instance"

def test_invalid_string_method():
    code = 'var s = "text"; s.invalidMethod();'
    interpreter = run(code)
    with pytest.raises(AttributeError):
        interpreter.execute()

def run(js_code):
    parser = Parser(js_code)
    ast = parser.parse_program()
    interpreter = Interpreter(ast)
    return interpreter

def test_string_methods_valid():
    code = '''
    var s = "Hello";
    s.toUpperCase();
    s.toLowerCase();
    s.substring(1,4);
    s.substr(1,2);
    s.charAt(0);
    '''
    interpreter = run(code)
    interpreter.execute()
    assert "s" in interpreter.environment

def test_string_method_invalid_args():
    code = 'var s = "abc"; s.charAt();'
    interpreter = run(code)
    with pytest.raises(TypeError):
        interpreter.execute()

def test_string_method_invalid_name():
    code = 'var s = "abc"; s.invalidMethod();'
    interpreter = run(code)
    with pytest.raises(AttributeError):
        interpreter.execute()

def test_array_methods_valid():
    code = '''
    var arr = [1];
    arr.push(2);
    arr.push(3,4);
    arr.pop();
    '''
    interpreter = run(code)
    interpreter.execute()
    assert len(interpreter.environment["arr"]) == 3

def test_array_method_invalid():
    code = 'var arr = [1]; arr.unknown();'
    interpreter = run(code)
    with pytest.raises(AttributeError):
        interpreter.execute()

def test_number_methods():
    code = '''
    var n = 12.345;
    n.toFixed(2);
    n.toString();
    '''
    interpreter = run(code)
    interpreter.execute()
    assert "n" in interpreter.environment

def test_number_method_invalid():
    code = 'var n = 42; n.badMethod();'
    interpreter = run(code)
    with pytest.raises(AttributeError):
        interpreter.execute()

def test_math_functions_all():
    code = '''
    Math.floor(4.7);
    Math.ceil(4.2);
    Math.round(4.5);
    Math.sqrt(16);
    Math.abs(-5);
    Math.max(1,2,3);
    Math.min(1,2,3);
    Math.pow(2,3);
    '''
    interpreter = run(code)
    interpreter.execute()

def test_special_values():
    code = "var a = null; var b = undefined; var c = true; var d = false;"
    interpreter = run(code)
    with pytest.raises(NameError):
        interpreter.execute()
