from ast_nodes.nodes import Literal, LambdaFunction, FunctionDeclaration
from errors.exceptions import TranspilerError


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
        node_type = node.__class__.__name__
        available_nodes = [
            'Program', 'VariableDeclaration', 'Literal', 'Identifier', 
            'BinaryOp', 'ConsoleLog', 'IfStatement', 'WhileStatement',
            'FunctionDeclaration', 'Comment', 'InlineComment'
        ]
        
        message = f"Nó '{node_type}' não tem método de transpilação implementado"
        message += f". Nós suportados: {', '.join(available_nodes)}"
        
        raise TranspilerError(node_type, message)

    def visit_Program(self, node):
        #code_lines = [self.visit(s) for s in node.statements]
        #code = "\n".join(code_lines)
        #
        #if 'math.' in code:
        #    return f"import math\n\n{code}"
        #else:
        #    return code
        
        statements = []
        prev_type = None
        
        for i, statement in enumerate(node.statements):
            current_code = self.visit(statement)
            current_type = statement.__class__.__name__
            
            # Adiciona quebra de linha entre diferentes tipos de declarações
            if prev_type and self._should_add_spacing(prev_type, current_type):
                statements.append("")
            
            statements.append(current_code)
            prev_type = current_type
            
        return "\n".join(statements)

    def _should_add_spacing(self, prev_type, current_type):
        """Determina se deve adicionar espaçamento entre tipos de declarações"""
        spacing_rules = {
            # Adiciona espaço antes de funções
            ('VariableDeclaration', 'FunctionDeclaration'),
            ('ConsoleLog', 'FunctionDeclaration'),
            ('Comment', 'FunctionDeclaration'),
            ('InlineComment', 'FunctionDeclaration'),
            
            # Adiciona espaço antes de classes
            ('VariableDeclaration', 'ClassDeclaration'),
            ('ConsoleLog', 'ClassDeclaration'),
            ('Comment', 'ClassDeclaration'),
            
            # Adiciona espaço após comentários multilinha grandes
            ('Comment', 'VariableDeclaration'),
            ('Comment', 'ConsoleLog'),
            
            # Adiciona espaço entre grupos de declarações
            ('FunctionDeclaration', 'VariableDeclaration'),
            ('FunctionDeclaration', 'ConsoleLog'),
            ('ClassDeclaration', 'VariableDeclaration'),
            
            # Adiciona espaço após blocos inline comments
            ('InlineComment', 'Comment'),
            ('InlineComment', 'FunctionDeclaration'),
        }
        
        return (prev_type, current_type) in spacing_rules

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
        
        # Operações simples que não precisam de parênteses
        simple_ops = {'+', '-', '*', '/', '%'}
        
        if node.op in op_map:
            py_op = op_map[node.op]
            # Comparações e operações lógicas só precisam de parênteses se necessário
            if self._needs_parentheses(node):
                return f"({left} {py_op} {right})"
            else:
                return f"{left} {py_op} {right}"

        if node.op == '+':
            # Em JavaScript, '+' com qualquer string faz concatenação
            # Vamos sempre usar str() para garantir concatenação correta
            if self.might_be_string_concatenation(node.left) or self.might_be_string_concatenation(node.right):
                return f"str({left}) + str({right})"
        
        # Para operações aritméticas simples, não usar parênteses desnecessários
        if node.op in simple_ops:
            return f"{left} {node.op} {right}"
            
        return f"({left} {node.op} {right})"

    def _needs_parentheses(self, node):
        """Determina se uma operação binária precisa de parênteses"""
        # Por enquanto, vamos ser conservadores e usar parênteses para operações lógicas
        return node.op in ['&&', '||', 'and', 'or']

    def might_be_string_concatenation(self, node):
        if isinstance(node, Literal) and isinstance(node.value, str):
            return True
        if hasattr(node, 'op') and node.op == '+':
            return True
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
        
        # Formatação melhorada para funções
        function_header = f"def {node.name}({params}):"
        indented_body = self._indent(body)
        
        return f"{function_header}\n{indented_body}"

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
        if node.is_multiline:
            lines = node.text.split('\n')
            if len(lines) == 1:
                return f"# {node.text}"
            else:
                # Formatação mais limpa para comentários multilinha
                formatted_lines = []
                formatted_lines.append("# " + "-" * 40)
                for line in lines:
                    text = line.strip()
                    if text:
                        formatted_lines.append(f"# {text}")
                    else:
                        formatted_lines.append("#")
                formatted_lines.append("# " + "-" * 40)
                return '\n'.join(formatted_lines)
        else:
            return f"# {node.text}"

    def visit_InlineComment(self, node):
        statement_code = self.visit(node.statement)
        return f"{statement_code}  # {node.comment_text}"

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
        
        elif node.method_name == 'toLowerCase':
            return f"{obj}.lower()"
        
        elif node.method_name == 'toUpperCase':
            return f"{obj}.upper()"
        
        elif node.method_name == 'push':
            args_str = ", ".join(args)
            return f"{obj}.append({args_str})"
        
        elif node.method_name == 'pop':
            return f"{obj}.pop()"
        
        elif obj == 'Math' and node.method_name == 'floor':
            return f"math.floor({args[0]})" if args else "math.floor"
        
        elif obj == 'Math' and node.method_name == 'ceil':
            return f"math.ceil({args[0]})" if args else "math.ceil"
        
        elif obj == 'Math' and node.method_name == 'round':
            return f"round({args[0]})" if args else "round"
        
        elif obj == 'Math' and node.method_name == 'abs':
            return f"abs({args[0]})" if args else "abs"
        
        elif obj == 'Math' and node.method_name == 'max':
            args_str = ", ".join(args)
            return f"max({args_str})"
        
        elif obj == 'Math' and node.method_name == 'min':
            args_str = ", ".join(args)
            return f"min({args_str})"
        
        elif obj == 'Math' and node.method_name == 'pow':
            return f"pow({args[0]}, {args[1]})" if len(args) >= 2 else "pow"
        
        elif obj == 'Math' and node.method_name == 'sqrt':
            return f"math.sqrt({args[0]})" if args else "math.sqrt"
        
        elif node.method_name == 'toFixed':
            return f"f\"{{{obj}:.{args[0]}f}}\"" if args else f"str({obj})"
        
        elif node.method_name == 'toString':
            return f"str({obj})"
        
        else:
            args_str = ", ".join(args)
            return f"{obj}.{node.method_name}({args_str})"

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        
        if node.op == '!':
            return f"not {operand}"
        else:
            return f"{node.op}{operand}"

    def visit_UpdateExpression(self, node):
        operand = self.visit(node.operand)
        
        if hasattr(node.operand, 'property_name') and node.operand.property_name == 'length':
            array_obj = self.visit(node.operand.object)
            if node.operator == '--':
                return f"# Redimensionar array: {array_obj} reduzido em 1 elemento\nif len({array_obj}) > 0: {array_obj}.pop()"
            elif node.operator == '++':
                return f"# Expandir array: {array_obj} expandido com None\n{array_obj}.append(None)"
        
        if node.operator == '++':
            return f"{operand} = {operand} + 1"
        elif node.operator == '--':
            return f"{operand} = {operand} - 1"
        else:
            raise ValueError(f"Operador de update não suportado: {node.operator}")
