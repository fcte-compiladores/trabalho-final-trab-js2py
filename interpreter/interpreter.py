from ast_nodes.nodes import Literal

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.environment = {}

    def execute(self):
        return self.visit(self.ast)

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"O interpretador não sabe como visitar um nó do tipo {node.__class__.__name__}")

    # --- Métodos de Visita para Execução ---

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_VariableDeclaration(self, node):
        value = self.visit(node.value)
        self.environment[node.name] = value
        return value

    def visit_BinaryOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            return left_val / right_val
        elif node.op in ('==', '==='):
            return left_val == right_val
        elif node.op in ('!=', '!=='):
            return left_val != right_val
        elif node.op == '>':
            return left_val > right_val
        
        raise Exception(f"Operador desconhecido: {node.op}")

    def visit_Literal(self, node):
        return node.value

    def visit_Identifier(self, node):
        if node.name in self.environment:
            return self.environment[node.name]
        else:
            raise NameError(f"A variável '{node.name}' não foi definida.")

    def visit_ConsoleLog(self, node):
        value_to_print = self.visit(node.argument)
        print(value_to_print)

    def visit_IfStatement(self, node):
        condition_val = self.visit(node.condition)
        if condition_val:
            self.visit(node.then_block)
        elif node.else_block:
            self.visit(node.else_block)

    def visit_Block(self, node):
        for statement in node.statements:
            self.visit(statement)