import pytest
from parser.parser import Parser
from ast_nodes.nodes import *
from errors.exceptions import ParserError

def parse_code(code):
    return Parser(code).parse_program()

def test_parse_variable():
    ast = parse_code('var x = 5;')
    assert isinstance(ast.statements[0], VariableDeclaration)

def test_parse_if_else():
    code = 'if (x > 5) { x = 10; } else { x = 0; }'
    ast = parse_code(code)
    assert isinstance(ast.statements[0], IfStatement)

def test_parse_while():
    code = 'while (x < 10) { x++; }'
    ast = parse_code(code)
    assert isinstance(ast.statements[0], WhileStatement)

def test_parse_function():
    code = 'function add(a,b) { return a + b; }'
    ast = parse_code(code)
    assert isinstance(ast.statements[0], FunctionDeclaration)

def test_parse_arrow_function():
    code = 'var dobro = (n) => n * 2;'
    ast = parse_code(code)
    assert isinstance(ast.statements[0].value, LambdaFunction)

def test_parse_array_object():
    code = 'var arr = [1,2,3]; var obj = { a: 1, b: 2 };'
    ast = parse_code(code)
    assert isinstance(ast.statements[0].value, ArrayLiteral)
    assert isinstance(ast.statements[1].value, ObjectLiteral)

def test_parse_for_each():
    code = 'for (var i of arr) { console.log(i); }'
    ast = parse_code(code)
    assert isinstance(ast.statements[0], ForEachStatement)

def test_parse_class():
    code = 'class Pessoa { constructor(nome) { this.nome = nome; } falar() { console.log(this.nome); } }'
    ast = parse_code(code)
    assert isinstance(ast.statements[0], ClassDeclaration)

def test_parse_for_and_assignments():
    code = "for (var i = 0; i < 3; i++) { arr[0] = 1; obj.key = 5; }"
    parser = Parser(code)
    ast = parser.parse_program()
    assert ast.statements[0].__class__.__name__ == "ForStatement"

def test_parse_new_and_this():
    code = "var obj = new Pessoa(1,2); this.nome = 'João';"
    parser = Parser(code)
    ast = parser.parse_program()
    names = [stmt.__class__.__name__ for stmt in ast.statements]
    assert "NewExpression" in names or "VariableDeclaration" in names

def test_parse_arrow_function_and_inline_comment():
    code = "var dobro = (n) => n * 2; // comentário"
    ast = Parser(code).parse_program()
    assert ast.statements[0].__class__.__name__ in ["VariableDeclaration","InlineComment"]

def test_parser_error_unexpected_token():
    code = "var x"
    with pytest.raises(ParserError):
        Parser(code).parse_program()

def test_parse_update_expressions():
    code = "i += 2; i -= 3;"
    ast = Parser(code).parse_program()
    assert len(ast.statements) == 2

def test_parse_invalid_for_each():
    code = "for (x something arr) {}"
    with pytest.raises(ParserError):
        Parser(code).parse_program()

def test_parse_array_assignment_invalid():
    code = "arr[0] = ;"
    with pytest.raises(SyntaxError):
        Parser(code).parse_program()
