from ast_nodes.nodes import Literal, LambdaFunction, FunctionDeclaration


class Transpiler:
    def __init__(self, ast):
        self.ast = ast

    def transpile(self):
        return self.visit(self.ast)

    def indent(self, code, level=1):
        indent_str = '    ' * level
        return '\n'.join(indent_str + line if line.strip() else line for line in code.split('\n'))

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method")

    def visit_Program(self, node):
        return "\n".join([self.visit(s) for s in node.statements])

    def visit_VariableDeclaration(self, node):
        if isinstance(node.value, LambdaFunction):
            return f"{node.name} = {self.visit(node.value)}"

        elif isinstance(node.value, FunctionDeclaration) and node.value.name is None:
            params = ', '.join(node.value.params)
            body = self.visit(node.value.body)
            return f"def {node.name}({params}):\n{self.indent(body)}"

        else:
            return f"{node.name} = {self.visit(node.value)}"

    def visit_Assignment(self, node):
        target = self.visit(node.target)
        value = self.visit(node.value)
        return f"{target} = {value}"

    def visit_Literal(self, node):
        if isinstance(node.value, str):
            return repr(node.value)
        elif isinstance(node.value, bool):
            return "True" if node.value else "False"
        else:
            return str(node.value)

    def visit_Identifier(self, node):
        return node.name

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        op_map = {
            '===': '==',
            '!==': '!=',
            '==':  '==',
            '!=':  '!=',
            '&&': 'and', 
            '||': 'or'
        }
        
        if node.op in op_map:
            py_op = op_map[node.op]
            return f"({left} {py_op} {right})"

        if node.op == '+':
            # Em JavaScript, '+' com qualquer string faz concatenação
            # Vamos sempre usar str() para garantir concatenação correta
            if self.might_be_string_concatenation(node.left) or self.might_be_string_concatenation(node.right):
                return f"(str({left}) + str({right}))"
        
        return f"({left} {node.op} {right})"

    def might_be_string_concatenation(self, node):
        # Verifica se um nó pode resultar em string ou concatenação
        if isinstance(node, Literal) and isinstance(node.value, str):
            return True
        if hasattr(node, 'op') and node.op == '+':
            return True  # Operações + podem ser concatenações
        return False


    def is_string(self, node):
        return isinstance(node, Literal) and isinstance(node.value, str)

    def visit_ConsoleLog(self, node):
        arg = self.visit(node.argument)
        return f"print({arg})"

    def visit_IfStatement(self, node):
        cond = self.visit(node.condition)
        then_block = self.visit(node.then_block)
        code = f"if {cond}:\n" + self._indent(then_block)
        if node.else_block:
            else_block = self.visit(node.else_block)
            code += f"\nelse:\n" + self._indent(else_block)
        return code

    def visit_WhileStatement(self, node):
        cond = self.visit(node.condition)
        body = self.visit(node.body)
        return f"while {cond}:\n" + self._indent(body)

    def visit_Block(self, node):
        return "\n".join([self.visit(s) for s in node.statements])

    def visit_FunctionDeclaration(self, node):
        params = ", ".join(node.params)
        body = self.visit(node.body)
        return f"def {node.name}({params}):\n" + self._indent(body)

    def visit_ReturnStatement(self, node):
        expr = self.visit(node.expression)
        return f"return {expr}"

    def visit_FunctionCall(self, node):
        args = ", ".join([self.visit(a) for a in node.arguments])
        return f"{node.name}({args})"

    def _indent(self, code, level=1):
        prefix = "    " * level
        return "\n".join(prefix + line for line in code.splitlines())
    
    def visit_ArrayLiteral(self, node):
        elements = [self.visit(e) for e in node.elements]
        return f"[{', '.join(elements)}]"

    def visit_ObjectLiteral(self, node):
        pairs = [f'"{k}": {self.visit(v)}' for k, v in node.pairs]
        return f"{{{', '.join(pairs)}}}"

    def visit_MemberAccess(self, node):
        obj = self.visit(node.object)
        if node.is_dot:
            key = self.visit(node.key)
            return f'{obj}[{key!r}]'
        else:
            index = self.visit(node.key)
            return f'{obj}[{index}]'

    def visit_LambdaFunction(self, node):
        params = ', '.join(node.params)
        return f"lambda {params}: {self.visit(node.expression)}"

    def visit_ForStatement(self, node):
        # Traduz for loop tradicional para while loop em Python
        init_code = ""
        if node.init:
            init_code = self.visit(node.init)
        
        condition = "True"
        if node.condition:
            condition = self.visit(node.condition)
        
        update_code = ""
        if node.update:
            update_code = self.visit(node.update)
        
        body = self.visit(node.body)
        
        # Se há update, adiciona ao final do corpo
        if update_code:
            if body.strip():
                body += f"\n{update_code}"
            else:
                body = update_code
        
        result = ""
        if init_code:
            result += f"{init_code}\n"
        
        result += f"while {condition}:\n{self._indent(body)}"
        
        return result

    def visit_ForEachStatement(self, node):
        iterable = self.visit(node.iterable)
        body = self.visit(node.body)

        loop_header = f"for {node.var} in {iterable}:"

        return f"{loop_header}\n{self._indent(body)}"

    def visit_Comment(self, node):
        return f"# {node.text}"

    def visit_ClassDeclaration(self, node):
        class_code = f"class {node.name}:"
        
        if not node.constructor and not node.methods:
            class_code += "\n    pass"
        else:
            if node.constructor:
                constructor_code = self.visit_ConstructorDeclaration(node.constructor)
                class_code += f"\n{self._indent(constructor_code)}"
            
            for method in node.methods:
                method_code = self.visit_MethodDeclaration(method)
                class_code += f"\n{self._indent(method_code)}"
        
        return class_code
    
    def visit_ConstructorDeclaration(self, node):
        params = ['self'] + node.params
        params_str = ', '.join(params)
        body = self.visit(node.body)

        if not body.strip():
            body = "pass"
        
        return f"def __init__({params_str}):\n{self._indent(body)}"
    
    def visit_MethodDeclaration(self, node):
        params = ['self'] + node.params
        params_str = ', '.join(params)
        body = self.visit(node.body)

        if not body.strip():
            body = "pass"
        
        return f"def {node.name}({params_str}):\n{self._indent(body)}"

    def visit_NewExpression(self, node):
        args = ", ".join([self.visit(arg) for arg in node.arguments])
        return f"{node.class_name}({args})"

    def visit_ThisExpression(self, node):
        return "self"

    def visit_PropertyAccess(self, node):
        obj = self.visit(node.object)
        if node.property_name == 'length':
            return f"len({obj})"
        return f"{obj}.{node.property_name}"

    def visit_MethodCall(self, node):
        obj = self.visit(node.object)
        args = [self.visit(arg) for arg in node.arguments]
        
        # Conversão de métodos JavaScript para Python
        if node.method_name == 'charAt':
            if len(args) == 1:
                return f"{obj}[{args[0]}] if 0 <= {args[0]} < len({obj}) else ''"
            else:
                raise TypeError("charAt() requer exatamente 1 argumento")
        
        elif node.method_name == 'substr':
            if len(args) == 1:
                return f"{obj}[{args[0]}:]"
            elif len(args) == 2:
                return f"{obj}[{args[0]}:{args[0]}+{args[1]}]"
            else:
                raise TypeError("substr() requer 1 ou 2 argumentos")
        
        elif node.method_name == 'substring':
            if len(args) == 1:
                return f"{obj}[{args[0]}:]"
            elif len(args) == 2:
                return f"{obj}[{args[0]}:{args[1]}]"
            else:
                raise TypeError("substring() requer 1 ou 2 argumentos")
        
        elif node.method_name == 'length':
            return f"len({obj})"
        
        elif node.method_name == 'push':
            # Para arrays
            args_str = ", ".join(args)
            return f"{obj}.append({args_str})"
        
        elif node.method_name == 'pop':
            return f"{obj}.pop()"
        
        else:
            # Método genérico
            args_str = ", ".join(args)
            return f"{obj}.{node.method_name}({args_str})"
