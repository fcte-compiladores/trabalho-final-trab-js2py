class Program:
    def __init__(self, statements):
        self.statements = statements

class VariableDeclaration:
    def __init__(self, name, value, kind='var'):  
        self.name = name
        self.value = value
        self.kind = kind

class Assignment:
    def __init__(self, target, value):
        self.target = target
        self.value = value

class Literal:
    def __init__(self, value):
        self.value = value

class Identifier:
    def __init__(self, name):
        self.name = name

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class ConsoleLog:
    def __init__(self, argument):
        self.argument = argument

class IfStatement:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Block:
    def __init__(self, statements):
        self.statements = statements

class FunctionDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnStatement:
    def __init__(self, expression):
        self.expression = expression

class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ArrayLiteral:
    def __init__(self, elements):
        self.elements = elements

class ObjectLiteral:
    def __init__(self, pairs):
        self.pairs = pairs

class MemberAccess:
    def __init__(self, object_, key, is_dot=False):
        self.object = object_
        self.key = key
        self.is_dot = is_dot

class LambdaFunction:
    def __init__(self, params, expression):
        self.params = params
        self.expression = expression

class ForEachStatement:
    def __init__(self, var, iterable, body, kind='of'):
        self.var = var
        self.iterable = iterable
        self.body = body
        self.kind = kind

class ForStatement:
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class Comment:
    def __init__(self, text, is_multiline=False):
        self.text = text
        self.is_multiline = is_multiline

class InlineComment:
    def __init__(self, statement, comment_text):
        self.statement = statement
        self.comment_text = comment_text

class ClassDeclaration:
    def __init__(self, name, constructor=None, methods=None):
        self.name = name
        self.constructor = constructor
        self.methods = methods or []
        
class ConstructorDeclaration:
    def __init__(self, params, body):
        self.params = params
        self.body = body

class MethodDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class NewExpression:
    def __init__(self, class_name, arguments):
        self.class_name = class_name
        self.arguments = arguments

class ThisExpression:
    def __init__(self):
        pass

class PropertyAccess:
    def __init__(self, object_, property_name):
        self.object = object_
        self.property_name = property_name

class MethodCall:
    def __init__(self, object_, method_name, arguments):
        self.object = object_
        self.method_name = method_name
        self.arguments = arguments

class UpdateExpression:
    def __init__(self, operator, operand, prefix=False):
        self.operator = operator
        self.operand = operand
        self.prefix = prefix