"""
Exceções personalizadas para o compilador JS→Python
Fornece informações detalhadas sobre erros de compilação e interpretação
"""

class CompilerError(Exception):
    """Exceção base para todos os erros do compilador"""
    def __init__(self, message, position=None, context=None, suggestion=None):
        self.message = message
        self.position = position
        self.context = context
        self.suggestion = suggestion
        super().__init__(self.format_error())
    
    def format_error(self):
        """Formata a mensagem de erro com informações detalhadas"""
        error_msg = f"💥 {self.message}"
        
        if self.position is not None:
            error_msg += f" (posição {self.position})"
        
        if self.context:
            error_msg += f"\n📍 Contexto: {self.context}"
        
        if self.suggestion:
            error_msg += f"\n💡 Sugestão: {self.suggestion}"
        
        return error_msg

class LexerError(CompilerError):
    """Erro durante a análise léxica (tokenização)"""
    def __init__(self, char, position, source_line=None):
        context = f"Caractere '{char}' não reconhecido"
        if source_line:
            context += f" na linha: {source_line}"
        
        suggestion = "Verifique se há caracteres especiais não suportados ou símbolos inválidos."
        
        super().__init__(
            "Erro na análise léxica",
            position=position,
            context=context,
            suggestion=suggestion
        )

class ParserError(CompilerError):
    """Erro durante a análise sintática"""
    def __init__(self, expected, found, position=None, context=None):
        message = f"Erro de sintaxe"
        
        if context:
            error_context = f"Esperado '{expected}', mas encontrado '{found}'. {context}"
        else:
            error_context = f"Esperado '{expected}', mas encontrado '{found}'"
        
        # Sugestões baseadas no tipo de erro
        suggestion = self._get_suggestion(expected, found)
        
        super().__init__(
            message,
            position=position,
            context=error_context,
            suggestion=suggestion
        )
    
    def _get_suggestion(self, expected, found):
        """Retorna sugestões específicas baseadas no erro"""
        suggestions = {
            ';': "Adicione ponto e vírgula ';' ao final da linha",
            ')': "Verifique se todos os parênteses estão balanceados",
            '}': "Verifique se todas as chaves estão balanceadas",
            ']': "Verifique se todos os colchetes estão balanceados",
            '=': "Use '=' para atribuição de valores",
            'IDENTIFIER': "Use um nome válido para variável (letras, números, _)",
        }
        
        return suggestions.get(expected, "Verifique a sintaxe do JavaScript")

class InterpreterError(CompilerError):
    """Erro durante a interpretação/execução"""
    def __init__(self, message, context=None, variable_state=None):
        suggestion = "Verifique os valores das variáveis e a lógica do programa"
        
        if variable_state:
            context = f"{context or message}. Estado das variáveis: {variable_state}"
        
        super().__init__(
            "Erro durante a execução",
            context=context,
            suggestion=suggestion
        )

class TranspilerError(CompilerError):
    """Erro durante a transpilação"""
    def __init__(self, node_type, message=None):
        default_msg = f"Não foi possível transpilar o nó do tipo '{node_type}'"
        actual_msg = message or default_msg
        
        suggestion = "Este recurso pode não estar implementado ainda no transpilador"
        
        super().__init__(
            "Erro na transpilação",
            context=actual_msg,
            suggestion=suggestion
        )
