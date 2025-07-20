from parser.parser import Parser
from interpreter.interpreter import Interpreter 
from errors.exceptions import CompilerError, LexerError, ParserError, InterpreterError
import sys
import traceback

def main():
    if len(sys.argv) < 2:
        print("Uso: python mainIn.py <arquivo_entrada.js>")
        print("Exemplo: python mainIn.py examples/demo_formatacao.js")
        return

    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {input_file}")
        print("Verifique se o caminho está correto e se o arquivo existe")
        return
    except UnicodeDecodeError:
        print(f"Erro de codificação no arquivo: {input_file}")
        print("Certifique-se de que o arquivo está em UTF-8")
        return

    print(f"Executando o arquivo: {input_file}")
    print("=" * 50)

    try:
        parser = Parser(code)
        ast = parser.parse_program()

        interpreter = Interpreter(ast)
        interpreter.execute()

        print("=" * 50)
        print("Execução concluída com sucesso!")

    except (LexerError, ParserError, InterpreterError) as e:
        print(str(e))
        print(f"\nArquivo: {input_file}")
        
    except Exception as e:
        print(f"Erro inesperado durante a execução: {e}")
        print(f"Arquivo: {input_file}")
        print("Detalhes técnicos:")
        traceback.print_exc()

if __name__ == "__main__":
    main()