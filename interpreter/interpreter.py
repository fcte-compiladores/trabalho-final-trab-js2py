from ast_nodes.nodes import Literal, Identifier, MemberAccess, PropertyAccess
import math

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.environment = {}
        self._setup_builtins()
    
    def _setup_builtins(self):
        """Configura objetos e funções built-in do JavaScript"""
        math_obj = {
            'type': 'object',
            'properties': {
                'floor': math.floor,
                'ceil': math.ceil,
                'round': round,
                'abs': abs,
                'max': max,
                'min': min,
                'pow': pow,
                'sqrt': math.sqrt,
                'PI': math.pi,
                'E': math.e
            }
        }
        self.environment['Math'] = math_obj

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
        elif node.name.startswith('this.'):
            property_name = node.name[5:]
            if 'this' in self.environment:
                this_obj = self.environment['this']
                this_obj[property_name] = value
                return value
            else:
                raise NameError("'this' não está definido no contexto atual")
        else:
            self.environment[node.name] = value
            return value

    def visit_Assignment(self, node):
        value = self.visit(node.value)
        
        if isinstance(node.target, Identifier):
            self.environment[node.target.name] = value
        elif isinstance(node.target, MemberAccess):
            obj = self.visit(node.target.object)
            key = self.visit(node.target.key)
            
            if isinstance(obj, list):
                if isinstance(key, (int, float)):
                    index = int(key)
                    if 0 <= index < len(obj):
                        obj[index] = value
                    else:
                        raise IndexError(f"Índice {index} fora dos limites do array")
                else:
                    raise TypeError("Índice de array deve ser numérico")
            elif isinstance(obj, dict):
                obj[key] = value
            else:
                raise TypeError("Só é possível atribuir a arrays ou objetos")
        elif isinstance(node.target, PropertyAccess):
            obj = self.visit(node.target.object)
            property_name = node.target.property_name
            
            if isinstance(obj, dict):
                if obj.get('type') == 'instance':
                    obj['properties'][property_name] = value
                else:
                    obj[property_name] = value
            else:
                raise TypeError("Só é possível atribuir propriedades a objetos")
        else:
            raise SyntaxError("Target de atribuição inválido")
        
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
        elif node.op == '%':
            if right_val == 0:
                return float('nan')
            return left_val % right_val
        elif node.op in ('==', '==='):
            return left_val == right_val
        elif node.op in ('!=', '!=='):
            return left_val != right_val
        elif node.op == '>':
            if left_val is None or right_val is None:
                return False
            return left_val > right_val
        elif node.op == '<':
            if left_val is None or right_val is None:
                return False
            return left_val < right_val
        elif node.op == '>=':
            if left_val is None or right_val is None:
                return False
            return left_val >= right_val
        elif node.op == '<=':
            if left_val is None or right_val is None:
                return False
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
        self.environment = self.environment.copy()
        
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

    def visit_ForStatement(self, node):
        loop_var_name = None
        loop_var_old_value = None
        
        if node.init and hasattr(node.init, 'name'):
            loop_var_name = node.init.name
            if loop_var_name in self.environment:
                loop_var_old_value = self.environment[loop_var_name]
        
        try:

            if node.init:
                self.visit(node.init)

            while True:
                if node.condition:
                    condition_result = self.visit(node.condition)
                    if not condition_result:
                        break

                self.visit(node.body)

                if node.update:
                    self.visit(node.update)
        finally:
            if loop_var_name:
                if loop_var_old_value is not None:
                    self.environment[loop_var_name] = loop_var_old_value
                else:
                    if loop_var_name in self.environment:
                        del self.environment[loop_var_name]

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
            raise NameError(f"Construtor '{node.class_name}' não foi definido.")
        
        constructor = self.environment[node.class_name]
        
        if isinstance(constructor, dict) and constructor.get('type') == 'class':
            instance = {
                'type': 'instance',
                'class': node.class_name,
                'properties': {}
            }
            
            if constructor['constructor']:
                args = [self.visit(arg) for arg in node.arguments]
                
                old_env = self.environment
                self.environment = self.environment.copy()
                self.environment['this'] = instance
                
                for i, param in enumerate(constructor['constructor'].params):
                    if i < len(args):
                        self.environment[param] = args[i]
                    else:
                        self.environment[param] = None
                
                try:
                    self.visit(constructor['constructor'].body)
                except ReturnException:
                    pass
                finally:
                    self.environment = old_env
            
            return instance
        
        elif isinstance(constructor, dict) and constructor.get('type') == 'function':
            instance = {}
            args = [self.visit(arg) for arg in node.arguments]
            
            old_env = self.environment
            self.environment = self.environment.copy()
            self.environment['this'] = instance
            
            for i, param in enumerate(constructor['params']):
                if i < len(args):
                    self.environment[param] = args[i]
                else:
                    self.environment[param] = None
            
            try:
                self.visit(constructor['body'])
            except ReturnException:
                pass
            finally:
                self.environment = old_env
            
            return instance
        
        else:
            raise TypeError(f"'{node.class_name}' não é um construtor válido.")
            
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

        if isinstance(obj, list) and node.property_name == 'length':
            return len(obj)

        if isinstance(obj, str) and node.property_name == 'length':
            return len(obj)

        if isinstance(obj, dict):
            if obj.get('type') == 'instance':
                return obj['properties'].get(node.property_name, None)
            else:
                return obj.get(node.property_name, None)
        
        raise TypeError(f"Propriedade '{node.property_name}' não encontrada para tipo {type(obj)}")

    def visit_MethodCall(self, node):
        obj = self.visit(node.object)
        
        if isinstance(obj, str):
            return self.handle_string_method(obj, node.method_name, node.arguments)

        if isinstance(obj, list):
            return self.handle_array_method(obj, node.method_name, node.arguments)
        
        if isinstance(obj, (int, float)):
            return self.handle_number_method(obj, node.method_name, node.arguments)
        
        if isinstance(obj, dict) and obj.get('type') == 'function' and node.method_name == 'call':
            args = [self.visit(arg) for arg in node.arguments]
            if len(args) == 0:
                raise TypeError("call() requer pelo menos um argumento (this)")

            new_this = args[0]
            function_args = args[1:]
            
            old_env = self.environment
            self.environment = self.environment.copy()
            self.environment['this'] = new_this
            
            for i, param in enumerate(obj['params']):
                if i < len(function_args):
                    self.environment[param] = function_args[i]
                else:
                    self.environment[param] = None
            
            try:
                self.visit(obj['body'])
                result = None
            except ReturnException as e:
                result = e.value
            finally:
                self.environment = old_env
            
            return result

        if isinstance(obj, dict) and obj.get('type') == 'object':
            if node.method_name in obj['properties']:
                method = obj['properties'][node.method_name]
                if callable(method):
                    args = [self.visit(arg) for arg in node.arguments]
                    return method(*args)
                else:
                    return method
            else:
                raise AttributeError(f"Método '{node.method_name}' não encontrado no objeto")
        
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

    def handle_string_method(self, string_obj, method_name, arguments):
        args = [self.visit(arg) for arg in arguments]
        
        if method_name == 'charAt':
            if len(args) != 1:
                raise TypeError("charAt() requer exatamente 1 argumento")
            index = args[0]
            if not isinstance(index, (int, float)):
                raise TypeError("charAt() requer um índice numérico")
            index = int(index)
            return string_obj[index] if 0 <= index < len(string_obj) else ""
        
        elif method_name == 'substr':
            if len(args) == 1:
                start = int(args[0])
                return string_obj[start:] if start >= 0 else ""
            elif len(args) == 2:
                start = int(args[0])
                length = int(args[1])
                return string_obj[start:start+length] if start >= 0 else ""
            else:
                raise TypeError("substr() requer 1 ou 2 argumentos")
        
        elif method_name == 'substring':
            if len(args) == 1:
                start = int(args[0])
                return string_obj[start:]
            elif len(args) == 2:
                start = int(args[0])
                end = int(args[1])
                return string_obj[start:end]
            else:
                raise TypeError("substring() requer 1 ou 2 argumentos")
        
        elif method_name == 'length':
            return len(string_obj)
        
        elif method_name == 'toLowerCase':
            return string_obj.lower()
        
        elif method_name == 'toUpperCase':
            return string_obj.upper()
        
        else:
            raise AttributeError(f"Método '{method_name}' não encontrado para string")

    def handle_array_method(self, array_obj, method_name, arguments):
        args = [self.visit(arg) for arg in arguments]
        
        if method_name == 'push':
            for arg in args:
                array_obj.append(arg)
            return len(array_obj)
        
        elif method_name == 'pop':
            return array_obj.pop() if array_obj else None
        
        elif method_name == 'length':
            return len(array_obj)
        
        else:
            raise AttributeError(f"Método '{method_name}' não encontrado para array")

    def handle_number_method(self, number_obj, method_name, arguments):
        args = [self.visit(arg) for arg in arguments]
        
        if method_name == 'toFixed':
            if len(args) != 1:
                raise TypeError("toFixed() requer exatamente 1 argumento")
            digits = int(args[0])
            return f"{number_obj:.{digits}f}"
        
        elif method_name == 'toString':
            return str(number_obj)
        
        else:
            raise AttributeError(f"Método '{method_name}' não encontrado para número")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        
        if node.op == '!':
            if operand is None or operand is False or operand == 0 or operand == "" or operand != operand:
                return True
            else:
                return False
        elif node.op == '-':
            return -operand
        elif node.op == '+':
            return +operand
        else:
            raise ValueError(f"Operador unário não suportado: {node.op}")

    def visit_UpdateExpression(self, node):
        if isinstance(node.operand, Identifier):
            current_value = self.environment.get(node.operand.name, 0)
            
            if node.operator == '++':
                new_value = current_value + 1
            elif node.operator == '--':
                new_value = current_value - 1
            else:
                raise ValueError(f"Operador de update não suportado: {node.operator}")
            
            self.environment[node.operand.name] = new_value

            return new_value if node.prefix else current_value
            
        else:
            from ast_nodes.nodes import PropertyAccess
            if isinstance(node.operand, PropertyAccess):
                obj = self.visit(node.operand.object)
                prop_name = node.operand.property_name

                if isinstance(obj, list) and prop_name == 'length':
                    current_length = len(obj)
                    
                    if node.operator == '--':
                        new_length = current_length - 1
                        if new_length >= 0:
                            while len(obj) > new_length:
                                obj.pop()
                        return new_length if node.prefix else current_length
                    elif node.operator == '++':
                        new_length = current_length + 1
                        obj.append(None)
                        return new_length if node.prefix else current_length
                
                if isinstance(obj, dict):
                    current_value = obj.get(prop_name, 0)
                elif isinstance(obj, list) and prop_name == 'length':
                    current_value = len(obj)
                else:
                    current_value = getattr(obj, prop_name, 0)
                
                if node.operator == '++':
                    new_value = current_value + 1
                elif node.operator == '--':
                    new_value = current_value - 1
                else:
                    raise ValueError(f"Operador de update não suportado: {node.operator}")
                
                if isinstance(obj, dict):
                    obj[prop_name] = new_value
                else:
                    setattr(obj, prop_name, new_value)
                
                return new_value if node.prefix else current_value
            else:
                raise TypeError(f"Update expression não suportado para {type(node.operand)}")

class ReturnException(Exception):
    """Exceção usada para implementar return statements"""
    def __init__(self, value):
        self.value = value