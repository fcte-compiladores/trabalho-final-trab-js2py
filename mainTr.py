from parser.parser import Parser
from translator.transpiler import Transpiler
from errors.exceptions import CompilerError, LexerError, ParserError, TranspilerError
import sys
import traceback

def main():
    if len(sys.argv) < 2:
        print("🔧 Uso: python mainTr.py <arquivo_entrada.js>")
        print("📝 Exemplo: python mainTr.py examples/demo_formatacao.js")
        return

    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {input_file}")
        print("💡 Verifique se o caminho está correto e se o arquivo existe")
        return
    except UnicodeDecodeError:
        print(f"❌ Erro de codificação no arquivo: {input_file}")
        print("💡 Certifique-se de que o arquivo está em UTF-8")
        return

    try:
        parser = Parser(code)
        ast = parser.parse_program()

        transpiler = Transpiler(ast)
        python_code = transpiler.transpile()

        # Cabeçalho mais elegante
        print("=" * 60)
        print("🐍 CÓDIGO PYTHON TRANSPILADO")
        print("=" * 60)
        print()
        print(python_code)
        print()
        print("=" * 60)

    except (LexerError, ParserError, TranspilerError) as e:
        print(str(e))
        print(f"\n📁 Arquivo: {input_file}")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print(f"📁 Arquivo: {input_file}")
        print("🐛 Detalhes técnicos:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
