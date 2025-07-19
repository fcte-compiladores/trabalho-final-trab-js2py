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
        
        if node.name.startswith('self.'):
            property_name = node.name[5:]
            if 'this' in self.environment:
                this_obj = self.environment['this']
                if isinstance(this_obj, dict) and this_obj.get('type') == 'instance':
                    this_obj['properties'][property_name] = value
                    return value
                else:
                    raise TypeError("'self' só pode ser usado em contexto de instância")
            else:
                raise NameError("'self' não está definido no contexto atual")
        else:
            self.environment[node.name] = value
            return value

    def visit_BinaryOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if node.op == '+':
            if isinstance(left_val, str) or isinstance(right_val, str):
                return str(left_val) + str(right_val)
            else:
                return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            if right_val == 0:
                return float('inf') if left_val > 0 else float('-inf') if left_val < 0 else float('nan')
            return left_val / right_val
        elif node.op in ('==', '==='):
            return left_val == right_val
        elif node.op in ('!=', '!=='):
            return left_val != right_val
        elif node.op == '>':
            return left_val > right_val
        elif node.op == '<':
            return left_val < right_val
        elif node.op == '>=':
            return left_val >= right_val
        elif node.op == '<=':
            return left_val <= right_val
        elif node.op == '&&':
            return left_val and right_val
        elif node.op == '||':
            return left_val or right_val
        
        raise Exception(f"Operador desconhecido: {node.op}")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        
        if node.op == '-':
            return -operand
        elif node.op == '+':
            return +operand
        elif node.op == '!':
            return not operand
        elif node.op == '++':
            return operand + 1
        elif node.op == '--':
            return operand - 1
        
        raise Exception(f"Operador unário desconhecido: {node.op}")

    def visit_Assignment(self, node):
        value = self.visit(node.value)
        
        if hasattr(node.target, 'object') and hasattr(node.target, 'property'):
            obj = self.visit(node.target.object)
            if isinstance(obj, dict) and obj.get('type') == 'instance':
                obj['properties'][node.target.property] = value
                return value
            else:
                raise TypeError("Atribuição a propriedade só é válida em instâncias")
        

        elif hasattr(node, 'target') and hasattr(node.target, 'name'):
            self.environment[node.target.name] = value
            return value
        
        raise Exception(f"Tipo de atribuição não suportado: {type(node.target)}")

    def visit_AssignmentExpression(self, node):
        return self.visit_Assignment(node)

    def visit_Literal(self, node):
        if node.value == 'null':
            return None
        elif node.value == 'undefined':
            return None
        elif node.value == 'true':
            return True
        elif node.value == 'false':
            return False
        return node.value

    def visit_Identifier(self, node):
        if node.name in self.environment:
            return self.environment[node.name]
        else:
            raise NameError(f"A variável '{node.name}' não foi definida.")

    def visit_ConsoleLog(self, node):
        value_to_print = self.visit(node.argument)
        if isinstance(value_to_print, dict) and value_to_print.get('type') == 'instance':
            print(f"[object {value_to_print['class']}]")
        else:
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

    def visit_Comment(self, node):
        pass

    def visit_WhileStatement(self, node):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_FunctionDeclaration(self, node):
        self.environment[node.name] = {
            'type': 'function',
            'params': node.params,
            'body': node.body,
            'environment': self.environment.copy()
        }

    def visit_ReturnStatement(self, node):
        value = self.visit(node.expression) if node.expression else None
        raise ReturnException(value)

    def visit_FunctionCall(self, node):
        if node.name not in self.environment:
            raise NameError(f"Função '{node.name}' não foi definida.")
        
        func = self.environment[node.name]
        if func.get('type') != 'function':
            raise TypeError(f"'{node.name}' não é uma função.")
        
        args = [self.visit(arg) for arg in node.arguments]
        
        old_env = self.environment
        self.environment = func['environment'].copy()
        
        for i, param in enumerate(func['params']):
            if i < len(args):
                self.environment[param] = args[i]
            else:
                self.environment[param] = None
        
        try:
            self.visit(func['body'])
            result = None
        except ReturnException as e:
            result = e.value
        finally:
            self.environment = old_env
        
        return result

    def visit_ArrayLiteral(self, node):
        return [self.visit(element) for element in node.elements]

    def visit_ObjectLiteral(self, node):
        obj = {}
        for key, value in node.pairs:
            obj_key = key if isinstance(key, str) else self.visit(key)
            obj[obj_key] = self.visit(value)
        return obj

    def visit_MemberAccess(self, node):
        obj = self.visit(node.object)
        if node.is_dot:
            key = node.key
        else:
            key = self.visit(node.key)
        
        if isinstance(obj, dict):
            if obj.get('type') == 'instance':
                return obj['properties'].get(key, None)
            else:
                return obj.get(key, None)
        elif isinstance(obj, list) and isinstance(key, int):
            return obj[key] if 0 <= key < len(obj) else None
        else:
            raise TypeError(f"Não é possível acessar propriedade de {type(obj)}")

    def visit_LambdaFunction(self, node):
        return {
            'type': 'lambda',
            'params': node.params,
            'expression': node.expression,
            'environment': self.environment.copy()
        }

    def visit_ForEachStatement(self, node):
        iterable = self.visit(node.iterable)
        if not isinstance(iterable, (list, dict)):
            raise TypeError("For...of/in requer um iterável")
        
        old_env = self.environment.copy()
        
        try:
            if node.kind == 'of' and isinstance(iterable, list):
                for item in iterable:
                    self.environment[node.var] = item
                    self.visit(node.body)
            elif node.kind == 'in' and isinstance(iterable, dict):
                for key in iterable:
                    self.environment[node.var] = key
                    self.visit(node.body)
        finally:
            for key in old_env:
                if key in self.environment:
                    self.environment[key] = old_env[key]

    def visit_ClassDeclaration(self, node):
        self.environment[node.name] = {
            'type': 'class',
            'name': node.name,
            'constructor': node.constructor,
            'methods': {method.name: method for method in node.methods}
        }

    def visit_ConstructorDeclaration(self, node):
        pass

    def visit_MethodDeclaration(self, node):
        pass

    def visit_NewExpression(self, node):
        if node.class_name not in self.environment:
            raise NameError(f"Classe '{node.class_name}' não foi definida.")
        
        class_def = self.environment[node.class_name]
        if class_def.get('type') != 'class':
            raise TypeError(f"'{node.class_name}' não é uma classe.")
        
        instance = {
            'type': 'instance',
            'class': node.class_name,
            'properties': {}
        }
        
        if class_def['constructor']:
            args = [self.visit(arg) for arg in node.arguments]
            
            old_env = self.environment
            self.environment = self.environment.copy()
            self.environment['this'] = instance
            
            for i, param in enumerate(class_def['constructor'].params):
                if i < len(args):
                    self.environment[param] = args[i]
                else:
                    self.environment[param] = None
            
            try:
                self.visit(class_def['constructor'].body)
            finally:
                self.environment = old_env
        
        return instance

    def visit_ThisExpression(self, node):
        if 'this' not in self.environment:
            raise NameError("'this' só pode ser usado dentro de métodos ou constructors")
        return self.environment['this']

    def visit_PropertyAccess(self, node):
        obj = self.visit(node.object)
        if not isinstance(obj, dict) or obj.get('type') != 'instance':
            raise TypeError("Acesso a propriedade só é válido em instâncias")
        return obj['properties'].get(node.property_name, None)

    def visit_MethodCall(self, node):
        obj = self.visit(node.object)
        if not isinstance(obj, dict) or obj.get('type') != 'instance':
            raise TypeError("Chamada de método só é válida em instâncias")
        
        class_name = obj['class']
        if class_name not in self.environment:
            raise NameError(f"Classe '{class_name}' não encontrada")
        
        class_def = self.environment[class_name]
        if node.method_name not in class_def['methods']:
            raise AttributeError(f"Método '{node.method_name}' não encontrado na classe '{class_name}'")
        
        method = class_def['methods'][node.method_name]
        
        args = [self.visit(arg) for arg in node.arguments]
        
        old_env = self.environment
        self.environment = self.environment.copy()
        self.environment['this'] = obj

        for i, param in enumerate(method.params):
            if i < len(args):
                self.environment[param] = args[i]
            else:
                self.environment[param] = None
        
        try:
            self.visit(method.body)
            result = None
        except ReturnException as e:
            result = e.value
        finally:
            self.environment = old_env
        
        return result

class ReturnException(Exception):
    """Exceção usada para implementar return statements"""
    def __init__(self, value):
        self.value = value