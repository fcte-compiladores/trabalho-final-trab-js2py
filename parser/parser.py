from lexer.tokenizer import tokenize
from errors.exceptions import ParserError
from ast_nodes.nodes import (
    Program, VariableDeclaration, Assignment, Literal, Identifier,
    BinaryOp, UnaryOp, ConsoleLog, IfStatement, WhileStatement,
    Block, FunctionDeclaration, ReturnStatement, FunctionCall, 
    ArrayLiteral, ObjectLiteral, MemberAccess, LambdaFunction,
    ForEachStatement, ForStatement, Comment, InlineComment, ClassDeclaration, ConstructorDeclaration,
    MethodDeclaration, NewExpression, ThisExpression, PropertyAccess, MethodCall, UpdateExpression
)

class Parser:
    def __init__(self, code):
        self.tokens = tokenize(code)
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token and token.type == token_type:
            self.pos += 1
            return token
        else:
            # Informações contextuais mais detalhadas
            context = f"Tentando processar token na posição {self.pos}"
            if token:
                context += f". Token atual: {token.type} = '{token.value}'"
            else:
                context += ". Fim do arquivo inesperado"
            
            raise ParserError(
                expected=token_type,
                found=token.type if token else "EOF",
                position=self.pos,
                context=context
            )

    def parse_program(self):
        statements = []
        while self.current_token() is not None:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()
        if token.type == 'COMMENT':
            return self.parse_comment()
        elif token.type == 'MULTILINE_COMMENT':
            return self.parse_multiline_comment()
        elif token.type == 'CLASS':
            return self.parse_class_declaration()
        elif token.type in ('VAR', 'LET', 'CONST'):
            stmt = self.parse_variable_declaration()
            return self.check_for_inline_comment(stmt)
        elif token.type == 'CONSOLE':
            stmt = self.parse_console_log()
            return self.check_for_inline_comment(stmt)
        elif token.type == 'IF':
            return self.parse_if_statement()
        elif token.type == 'WHILE':
            return self.parse_while_statement()
        elif token.type == 'FUNCTION':
            return self.parse_function_declaration()
        elif token.type == 'RETURN':
            stmt = self.parse_return_statement()
            return self.check_for_inline_comment(stmt)
        elif token.type == 'THIS':
            stmt = self.parse_this_assignment()
            return self.check_for_inline_comment(stmt)
        elif token.type == 'IDENTIFIER':
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token.type == 'LPAREN':
                stmt = self.parse_function_call_statement()
                return self.check_for_inline_comment(stmt)
            elif next_token and next_token.type == 'DOT':
                stmt = self.parse_object_method_or_assignment()
                return self.check_for_inline_comment(stmt)
            elif next_token and next_token.type == 'LBRACKET':
                stmt = self.parse_array_assignment()
                return self.check_for_inline_comment(stmt)
            else:
                stmt = self.parse_assignment()
                return self.check_for_inline_comment(stmt)
        elif token.type == 'FOR':
            return self.parse_for_statement()
        else:
            # Melhor descrição de tokens inesperados
            available_tokens = ['VAR', 'LET', 'CONST', 'FUNCTION', 'IF', 'WHILE', 'FOR', 'RETURN', 'CLASS']
            context = f"Token '{token.type}' não é válido no início de uma declaração"
            context += f". Tokens válidos: {', '.join(available_tokens)}"
            
            raise ParserError(
                expected="declaração válida",
                found=token.type,
                position=self.pos,
                context=context
            )

    def parse_comment(self):
        token = self.eat('COMMENT')
        comment_text = token.value[2:].strip()
        return Comment(comment_text, is_multiline=False)

    def parse_multiline_comment(self):
        token = self.eat('MULTILINE_COMMENT')
        # Remove /* e */ e strip whitespace
        comment_text = token.value[2:-2].strip()
        return Comment(comment_text, is_multiline=True)

    def check_for_inline_comment(self, statement):
        """Verifica se há um comentário inline após o statement"""
        if self.current_token() and self.current_token().type == 'COMMENT':
            comment_token = self.eat('COMMENT')
            comment_text = comment_token.value[2:].strip()
            return InlineComment(statement, comment_text)
        return statement

    def parse_variable_declaration(self):
        kind = self.eat(self.current_token().type).value 
        ident = self.eat('IDENTIFIER')
        
        if self.current_token() and self.current_token().type == 'OP_ASSIGN':
            self.eat('OP_ASSIGN')

            if self.current_token().type == 'LPAREN':
                lookahead_pos = self.pos
                try:
                    self.eat('LPAREN')
                    while self.current_token().type != 'RPAREN':
                        self.eat(self.current_token().type)
                    self.eat('RPAREN')

                    if self.current_token().type == 'ARROW':
                        self.pos = lookahead_pos
                        func = self.parse_arrow_function()
                        if self.current_token() and self.current_token().type == 'SEMICOLON':
                            self.eat('SEMICOLON')
                        return VariableDeclaration(ident.value, func, kind)
                    else:
                        self.pos = lookahead_pos
                except:
                    self.pos = lookahead_pos

            value = self.parse_expression()
        else:
            value = Literal(None)
        
        self.eat('SEMICOLON')
        return VariableDeclaration(ident.value, value, kind)

    def parse_array_assignment(self):
        array_name = self.eat('IDENTIFIER').value
        self.eat('LBRACKET')
        index = self.parse_expression()
        self.eat('RBRACKET')
        
        token = self.current_token()
        if token.type == 'OP_ASSIGN':
            self.eat('OP_ASSIGN')
            value = self.parse_expression()
            self.eat('SEMICOLON')

            target = MemberAccess(Identifier(array_name), index)
            return Assignment(target, value)
        else:
            raise SyntaxError(f"Esperado '=' após acesso a array, encontrado {token}")

    def parse_assignment(self):
        ident = self.eat('IDENTIFIER')
        token = self.current_token()

        if token.type == 'OP_ASSIGN':
            self.eat('OP_ASSIGN')
            value = self.parse_expression()
            self.eat('SEMICOLON')
            return VariableDeclaration(ident.value, value)

        elif token.type in ('OP_PLUSEQ', 'OP_MINUSEQ'):
            op_token = self.eat(token.type)
            value = self.parse_expression()
            self.eat('SEMICOLON')
            op = op_token.value[0]
            expr = BinaryOp(Identifier(ident.value), op, value)
            return VariableDeclaration(ident.value, expr)

        elif token.type == 'OP_INCREMENT':
            self.eat('OP_INCREMENT')
            self.eat('SEMICOLON')
            expr = BinaryOp(Identifier(ident.value), '+', Literal(1))
            return VariableDeclaration(ident.value, expr)

        elif token.type == 'OP_DECREMENT':
            self.eat('OP_DECREMENT')
            self.eat('SEMICOLON')
            expr = BinaryOp(Identifier(ident.value), '-', Literal(1))
            return VariableDeclaration(ident.value, expr)

        else:
            raise SyntaxError(f"Operação não suportada: {token}")

    def parse_console_log(self):
        self.eat('CONSOLE')
        self.eat('DOT')
        self.eat('LOG')
        self.eat('LPAREN')
        arg = self.parse_expression()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        return ConsoleLog(arg)

    def parse_if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        then_block = self.parse_block()
        else_block = None
        if self.current_token() and self.current_token().type == 'ELSE':
            self.eat('ELSE')
            if self.current_token() and self.current_token().type == 'IF':
                else_block = Block([self.parse_if_statement()])
            else:
                else_block = self.parse_block()
        return IfStatement(condition, then_block, else_block)

    def parse_while_statement(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_block(self):
        self.eat('LBRACE')
        statements = []
        while self.current_token() and self.current_token().type != 'RBRACE':
            statements.append(self.parse_statement())
        self.eat('RBRACE')
        return Block(statements)

    def parse_function_declaration(self):
        self.eat('FUNCTION')
        name = self.eat('IDENTIFIER').value
        self.eat('LPAREN')
        params = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            params.append(self.eat('IDENTIFIER').value)
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENTIFIER').value)
        self.eat('RPAREN')
        body = self.parse_block()
        return FunctionDeclaration(name, params, body)

    def parse_return_statement(self):
        self.eat('RETURN')
        expr = self.parse_expression()
        self.eat('SEMICOLON')
        return ReturnStatement(expr)

    def parse_array(self):
        self.eat('LBRACKET')
        elements = []
        if self.current_token().type != 'RBRACKET':
            elements.append(self.parse_expression())
            while self.current_token().type == 'COMMA':
                self.eat('COMMA')
                elements.append(self.parse_expression())
        self.eat('RBRACKET')
        return ArrayLiteral(elements)
    
    def parse_object(self):
        self.eat('LBRACE')
        pairs = []
        if self.current_token().type != 'RBRACE':
            while True:
                key_token = self.eat('IDENTIFIER')
                self.eat('COLON')
                value = self.parse_expression()
                pairs.append((key_token.value, value))
                if self.current_token().type == 'COMMA':
                    self.eat('COMMA')
                else:
                    break
        self.eat('RBRACE')
        return ObjectLiteral(pairs)


    def parse_function_call_statement(self):
        call = self.parse_function_call()
        self.eat('SEMICOLON')
        return call

    def parse_function_call(self):
        name = self.eat('IDENTIFIER').value
        self.eat('LPAREN')
        args = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            args.append(self.parse_expression())
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                args.append(self.parse_expression())
        self.eat('RPAREN')
        return FunctionCall(name, args)

    def parse_expression(self):
      node = self.parse_add_sub()

      while self.current_token() and self.current_token().type in ('GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ', 'EQ_STRICT', 'NEQ_STRICT'):
          op_token = self.eat(self.current_token().type)
          right = self.parse_add_sub()
          node = BinaryOp(node, op_token.value, right)

      return node

    def parse_add_sub(self):
        node = self.parse_mul_div()
        while self.current_token() and self.current_token().type in ('OP_PLUS', 'OP_MINUS'):
            op = self.eat(self.current_token().type).value
            right = self.parse_mul_div()
            node = BinaryOp(node, op, right)
        return node

    def parse_mul_div(self):
        node = self.parse_primary()
        while self.current_token() and self.current_token().type in ('OP_MUL', 'OP_DIV', 'OP_MOD'):
            op = self.eat(self.current_token().type).value
            right = self.parse_primary()
            node = BinaryOp(node, op, right)
        return node

    def parse_arrow_function(self):
        self.eat('LPAREN')
        params = []
        if self.current_token().type != 'RPAREN':
            params.append(self.eat('IDENTIFIER').value)
            while self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENTIFIER').value)
        self.eat('RPAREN')
        self.eat('ARROW')

        if self.current_token().type == 'LBRACE':
            body = self.parse_block()
            return FunctionDeclaration(None, params, body)
        else:
            expr = self.parse_expression()
            return LambdaFunction(params, expr)

    def parse_for_statement(self):
        self.eat('FOR')
        self.eat('LPAREN')

        saved_pos = self.pos
        try:
            if self.current_token().type in ('VAR', 'LET', 'CONST'):
                decl_type = self.current_token().type
                self.eat(decl_type)
                var_name = self.eat('IDENTIFIER').value

                if self.current_token().type in ('IN', 'OF'):
                    self.pos = saved_pos
                    return self.parse_for_each()
                else:
                    self.pos = saved_pos
                    return self.parse_traditional_for()
            else:
                self.pos = saved_pos
                return self.parse_traditional_for()
        except:
            self.pos = saved_pos
            return self.parse_traditional_for()

    def parse_traditional_for(self):
        init = None
        if self.current_token().type in ('VAR', 'LET', 'CONST'):
            init = self.parse_variable_declaration_no_semicolon()
        elif self.current_token().type != 'SEMICOLON':
            init = self.parse_expression()
        self.eat('SEMICOLON')
        
        condition = None
        if self.current_token().type != 'SEMICOLON':
            condition = self.parse_expression()
        self.eat('SEMICOLON')

        update = None
        if self.current_token().type != 'RPAREN':
            update = self.parse_update_expression()
        self.eat('RPAREN')
        
        body = self.parse_block()
        
        return ForStatement(init, condition, update, body)

    def parse_update_expression(self):
        if self.current_token().type == 'IDENTIFIER':
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token.type in ('OP_INCREMENT', 'OP_DECREMENT', 'OP_PLUSEQ', 'OP_MINUSEQ', 'OP_ASSIGN'):
                ident = self.eat('IDENTIFIER')
                token = self.current_token()

                if token.type == 'OP_INCREMENT':
                    self.eat('OP_INCREMENT')
                    expr = BinaryOp(Identifier(ident.value), '+', Literal(1))
                    return VariableDeclaration(ident.value, expr)

                elif token.type == 'OP_DECREMENT':
                    self.eat('OP_DECREMENT')
                    expr = BinaryOp(Identifier(ident.value), '-', Literal(1))
                    return VariableDeclaration(ident.value, expr)

                elif token.type in ('OP_PLUSEQ', 'OP_MINUSEQ'):
                    op_token = self.eat(token.type)
                    value = self.parse_expression()
                    op = op_token.value[0]
                    expr = BinaryOp(Identifier(ident.value), op, value)
                    return VariableDeclaration(ident.value, expr)

                elif token.type == 'OP_ASSIGN':
                    self.eat('OP_ASSIGN')
                    value = self.parse_expression()
                    return VariableDeclaration(ident.value, value)

        return self.parse_expression()

    def parse_variable_declaration_no_semicolon(self):
        kind = self.eat(self.current_token().type).value 
        ident = self.eat('IDENTIFIER')
        
        if self.current_token() and self.current_token().type == 'OP_ASSIGN':
            self.eat('OP_ASSIGN')
            value = self.parse_expression()
        else:
            value = Literal(None)
        
        return VariableDeclaration(ident.value, value, kind)
    def parse_for_each(self):

        if self.current_token().type in ('VAR', 'LET', 'CONST'):
            self.eat(self.current_token().type)
        var_name = self.eat('IDENTIFIER').value

        kind_token = self.current_token()
        if kind_token.type == 'IN':
            self.eat('IN')
            kind = 'in'
        elif kind_token.type == 'OF':
            self.eat('OF')
            kind = 'of'
        else:
            raise SyntaxError(f"Esperado 'in' ou 'of', encontrado: {kind_token}")

        iterable = self.parse_expression()
        self.eat('RPAREN')

        body = self.parse_block()
        return ForEachStatement(var_name, iterable, body, kind)

    def parse_primary(self):
        token = self.current_token()
        if token.type == 'NOT':
            self.eat('NOT')
            operand = self.parse_primary()
            return UnaryOp('!', operand)
        elif token.type == 'OP_MINUS':
            self.eat('OP_MINUS')
            operand = self.parse_primary()
            return UnaryOp('-', operand)
        elif token.type == 'OP_PLUS':
            self.eat('OP_PLUS')
            operand = self.parse_primary()
            return UnaryOp('+', operand)
        elif token.type == 'NEW':
            return self.parse_new_expression()
        elif token.type == 'THIS':
            self.eat('THIS')
            node = ThisExpression()

            while self.current_token() and self.current_token().type == 'DOT':
                self.eat('DOT')
                property_name = self.eat('IDENTIFIER').value
                
                if self.current_token() and self.current_token().type == 'LPAREN':
                    self.eat('LPAREN')
                    args = []
                    if self.current_token() and self.current_token().type != 'RPAREN':
                        args.append(self.parse_expression())
                        while self.current_token() and self.current_token().type == 'COMMA':
                            self.eat('COMMA')
                            args.append(self.parse_expression())
                    self.eat('RPAREN')
                    node = MethodCall(node, property_name, args)
                else:
                    node = PropertyAccess(node, property_name)
            
            return node
        elif token.type == 'NUMBER':
            self.eat('NUMBER')
            value = float(token.value) if '.' in token.value else int(token.value)
            return Literal(value)
        elif token.type == 'STRING':
            self.eat('STRING')
            return Literal(token.value[1:-1])
        elif token.type == 'TRUE':
            self.eat('TRUE')
            return Literal(True)
        elif token.type == 'FALSE':
            self.eat('FALSE')
            return Literal(False)
        elif token.type == 'IDENTIFIER':
            node = Identifier(token.value)
            self.eat('IDENTIFIER')

            while self.current_token() and self.current_token().type in ('DOT', 'LBRACKET', 'LPAREN'):
                if self.current_token().type == 'DOT':
                    self.eat('DOT')
                    property_name = self.eat('IDENTIFIER').value
                    
                    if self.current_token() and self.current_token().type == 'LPAREN':
                        self.eat('LPAREN')
                        args = []
                        if self.current_token() and self.current_token().type != 'RPAREN':
                            args.append(self.parse_expression())
                            while self.current_token() and self.current_token().type == 'COMMA':
                                self.eat('COMMA')
                                args.append(self.parse_expression())
                        self.eat('RPAREN')
                        node = MethodCall(node, property_name, args)
                    else:
                        node = PropertyAccess(node, property_name)
                        
                elif self.current_token().type == 'LBRACKET':
                    self.eat('LBRACKET')
                    index = self.parse_expression()
                    self.eat('RBRACKET')
                    node = MemberAccess(node, index)
                
                elif self.current_token().type == 'LPAREN':
                    self.eat('LPAREN')
                    args = []
                    if self.current_token() and self.current_token().type != 'RPAREN':
                        args.append(self.parse_expression())
                        while self.current_token() and self.current_token().type == 'COMMA':
                            self.eat('COMMA')
                            args.append(self.parse_expression())
                    self.eat('RPAREN')
                    if isinstance(node, Identifier):
                        node = FunctionCall(node.name, args)
                    else:
                        node = MethodCall(node, None, args)
            return node
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()
            self.eat('RPAREN')
            return node
        elif token.type == 'LBRACKET':
            return self.parse_array()
        elif token.type == 'LBRACE':
            return self.parse_object()
        else:
            raise SyntaxError(f"Token inesperado em expressão: {token}")

    def parse_new_expression(self):
        self.eat('NEW')
        class_name = self.eat('IDENTIFIER').value
        self.eat('LPAREN')
        
        args = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            args.append(self.parse_expression())
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                args.append(self.parse_expression())
        
        self.eat('RPAREN')
        return NewExpression(class_name, args)

    def parse_this_assignment(self):
        self.eat('THIS')
        self.eat('DOT')
        property_name = self.eat('IDENTIFIER').value
        
        if self.current_token() and self.current_token().type == 'LPAREN':
            self.eat('LPAREN')
            args = []
            if self.current_token() and self.current_token().type != 'RPAREN':
                args.append(self.parse_expression())
                while self.current_token() and self.current_token().type == 'COMMA':
                    self.eat('COMMA')
                    args.append(self.parse_expression())
            self.eat('RPAREN')
            self.eat('SEMICOLON')
            
            this_obj = ThisExpression()
            return MethodCall(this_obj, property_name, args)
        elif self.current_token() and self.current_token().type == 'OP_ASSIGN':
            self.eat('OP_ASSIGN')
            value = self.parse_expression()
            self.eat('SEMICOLON')
            
            return VariableDeclaration(f"this.{property_name}", value)
        else:
            raise SyntaxError(f"Esperado '(' ou '=' após this.{property_name}, encontrado {self.current_token()}")

    def parse_object_method_or_assignment(self):
        saved_pos = self.pos

        try:
            expr = self.parse_expression()
            
            if self.current_token() and self.current_token().type in ('OP_ASSIGN', 'OP_PLUSEQ', 'OP_MINUSEQ', 'OP_MULEQ', 'OP_DIVEQ'):
                op_token = self.current_token()
                self.eat(op_token.type)
                value = self.parse_expression()
                self.eat('SEMICOLON')
                
                if op_token.type == 'OP_ASSIGN':
                    return Assignment(expr, value)
                else:
                    op_map = {
                        'OP_PLUSEQ': '+',
                        'OP_MINUSEQ': '-',
                        'OP_MULEQ': '*',
                        'OP_DIVEQ': '/'
                    }
                    binary_op = BinaryOp(expr, op_map[op_token.type], value)
                    return Assignment(expr, binary_op)
            
            elif self.current_token() and self.current_token().type in ('OP_INCREMENT', 'OP_DECREMENT'):
                op_token = self.current_token()
                self.eat(op_token.type)
                self.eat('SEMICOLON')
                return UpdateExpression(op_token.value, expr, prefix=False)
            
            elif self.current_token() and self.current_token().type == 'SEMICOLON':
                self.eat('SEMICOLON')
                return expr
            
            else:
                self.pos = saved_pos
                return self.parse_simple_object_access()
        
        except Exception:
            self.pos = saved_pos
            return self.parse_simple_object_access()
    
    def parse_simple_object_access(self):
        obj_name = self.eat('IDENTIFIER').value
        self.eat('DOT')
        property_name = self.eat('IDENTIFIER').value
        
        if self.current_token() and self.current_token().type == 'LPAREN':
            self.eat('LPAREN')
            args = []
            if self.current_token() and self.current_token().type != 'RPAREN':
                args.append(self.parse_expression())
                while self.current_token() and self.current_token().type == 'COMMA':
                    self.eat('COMMA')
                    args.append(self.parse_expression())
            self.eat('RPAREN')
            self.eat('SEMICOLON')
            
            obj = Identifier(obj_name)
            return MethodCall(obj, property_name, args)
        else:
            raise SyntaxError(f"Comportamento não esperado para {obj_name}.{property_name}")

    def parse_class_declaration(self):
        self.eat('CLASS')
        class_name = self.eat('IDENTIFIER').value
        self.eat('LBRACE')
        
        constructor = None
        methods = []
        
        while self.current_token() and self.current_token().type != 'RBRACE':
            token = self.current_token()
            
            if token.type == 'CONSTRUCTOR':
                constructor = self.parse_constructor()
            elif token.type == 'IDENTIFIER':
                method = self.parse_method()
                methods.append(method)
            elif token.type == 'COMMENT':
                self.eat('COMMENT')
            else:
                raise SyntaxError(f"Token inesperado dentro da classe: {token}")
        
        self.eat('RBRACE')
        return ClassDeclaration(class_name, constructor, methods)
    
    def parse_constructor(self):
        self.eat('CONSTRUCTOR')
        self.eat('LPAREN')
        
        params = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            params.append(self.eat('IDENTIFIER').value)
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENTIFIER').value)
        
        self.eat('RPAREN')
        body = self.parse_block()
        
        return ConstructorDeclaration(params, body)
    
    def parse_method(self):
        method_name = self.eat('IDENTIFIER').value
        self.eat('LPAREN')
        
        params = []
        if self.current_token() and self.current_token().type != 'RPAREN':
            params.append(self.eat('IDENTIFIER').value)
            while self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
                params.append(self.eat('IDENTIFIER').value)
        
        self.eat('RPAREN')
        body = self.parse_block()
        
        return MethodDeclaration(method_name, params, body)

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.current_token() and self.current_token().type == 'LOGICAL_OR':
            op_token = self.eat('LOGICAL_OR')
            right = self.parse_logical_and()
            node = BinaryOp(node, op_token.value, right)

        return node

    def parse_logical_and(self):
        node = self.parse_comparison()
        while self.current_token() and self.current_token().type == 'LOGICAL_AND':
            op_token = self.eat('LOGICAL_AND')
            right = self.parse_comparison()
            node = BinaryOp(node, op_token.value, right)

        return node

    def parse_comparison(self):
        node = self.parse_add_sub()
        while self.current_token() and self.current_token().type in (
            'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ', 'EQ_STRICT', 'NEQ_STRICT'
        ):
            op_token = self.eat(self.current_token().type)
            right = self.parse_add_sub()
            node = BinaryOp(node, op_token.value, right)

        return node
