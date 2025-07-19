#!/usr/bin/env python3
"""
Compilador JavaScript → Python
Script principal unificado para transpilação e interpretação

Uso:
    python main.py <arquivo.js> [opções]

Opções:
    -t, --transpile     Apenas transpila para Python (padrão)
    -i, --interpret     Apenas interpreta/executa o JavaScript
    -a, --all           Executa ambos: transpilação e interpretação
    -o, --output FILE   Salva o código Python transpilado em arquivo
    -v, --verbose       Modo verboso com informações detalhadas
    -h, --help          Mostra esta mensagem de ajuda

Exemplos:
    python main.py exemplo.js                    # Apenas transpila
    python main.py exemplo.js -i                 # Apenas interpreta
    python main.py exemplo.js -a                 # Transpila e interpreta
    python main.py exemplo.js -t -o saida.py     # Transpila e salva em arquivo
    python main.py exemplo.js -a -v              # Modo verboso completo
"""

import sys
import argparse
import traceback
from pathlib import Path

from parser.parser import Parser
from translator.transpiler import Transpiler
from interpreter.interpreter import Interpreter
from errors.exceptions import CompilerError, LexerError, ParserError, TranspilerError, InterpreterError


def print_banner():
    """Exibe o banner do compilador"""
    print("=" * 70)
    print("COMPILADOR JAVASCRIPT -> PYTHON")
    print("Transpilador e Interpretador Unificado")
    print("=" * 70)


def print_section(title, emoji=""):
    """Imprime uma seção com formatação"""
    print(f"\n{title}")
    print("-" * len(title))


def load_file(file_path, verbose=False):
    """Carrega e valida o arquivo de entrada"""
    if verbose:
        print(f"Carregando arquivo: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if verbose:
            lines = len(code.split('\n'))
            chars = len(code)
            print(f"   Arquivo carregado: {lines} linhas, {chars} caracteres")
        
        return code
    
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {file_path}")
        print("Verifique se o caminho esta correto e se o arquivo existe")
        return None
    
    except UnicodeDecodeError:
        print(f"Erro de codificacao no arquivo: {file_path}")
        print("Certifique-se de que o arquivo esta em UTF-8")
        return None


def transpile_code(code, verbose=False):
    """Transpila o código JavaScript para Python"""
    if verbose:
        print_section("TRANSPILACAO")
    
    try:
        parser = Parser(code)
        ast = parser.parse_program()
        
        if verbose:
            print("   Analise sintatica concluida")
        
        transpiler = Transpiler(ast)
        python_code = transpiler.transpile()
        
        if verbose:
            print("   Transpilacao concluida")
        
        return python_code
    
    except (LexerError, ParserError, TranspilerError) as e:
        print(str(e))
        return None


def interpret_code(code, verbose=False):
    """Interpreta/executa o código JavaScript"""
    if verbose:
        print_section("INTERPRETACAO")
    
    try:
        parser = Parser(code)
        ast = parser.parse_program()
        
        if verbose:
            print("   Analise sintatica concluida")
        
        interpreter = Interpreter(ast)
        
        if verbose:
            print("   Iniciando execucao...")
            print()
        
        interpreter.execute()
        
        if verbose:
            print()
            print("   Execucao concluida")
        
        return True
    
    except (LexerError, ParserError, InterpreterError) as e:
        print(str(e))
        return False


def save_to_file(content, output_file, verbose=False):
    """Salva o conteúdo em um arquivo"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if verbose:
            print(f"Codigo salvo em: {output_file}")
        else:
            print(f"Arquivo salvo: {output_file}")
    
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")


def create_parser():
    """Cria o parser de argumentos"""
    parser = argparse.ArgumentParser(
        description="Compilador JavaScript → Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py exemplo.js                     # Apenas transpila
  python main.py exemplo.js -i                  # Apenas interpreta
  python main.py exemplo.js -a                  # Transpila e interpreta
  python main.py exemplo.js -t -o saida.py      # Transpila e salva
  python main.py exemplo.js -a -v               # Modo verboso completo
        """
    )
    
    parser.add_argument(
        'file',
        help='Arquivo JavaScript de entrada'
    )
    
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '-t', '--transpile',
        action='store_true',
        help='Apenas transpila para Python (padrão)'
    )
    mode_group.add_argument(
        '-i', '--interpret',
        action='store_true',
        help='Apenas interpreta/executa o JavaScript'
    )
    mode_group.add_argument(
        '-a', '--all',
        action='store_true',
        help='Executa ambos: transpilação e interpretação'
    )
    
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        help='Salva o código Python transpilado em arquivo'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Modo verboso com informações detalhadas'
    )
    
    return parser


def main():
    """Função principal"""
    # Parse dos argumentos
    parser = create_parser()
    args = parser.parse_args()
    
    # Determina o modo de operação
    if args.interpret:
        mode = 'interpret'
    elif args.all:
        mode = 'both'
    else:
        mode = 'transpile'  # padrão
    
    # Exibe banner apenas se verbose
    if args.verbose:
        print_banner()
        print(f"Arquivo: {args.file}")
        print(f"Modo: {mode}")
        if args.output:
            print(f"Saida: {args.output}")
    
    # Carrega o arquivo
    code = load_file(args.file, args.verbose)
    if code is None:
        sys.exit(1)
    
    # Executa baseado no modo
    success = True
    python_code = None
    
    if mode in ['transpile', 'both']:
        python_code = transpile_code(code, args.verbose)
        if python_code is None:
            success = False
        else:
            if mode == 'transpile':
                # Exibe apenas o código transpilado quando for só transpilação
                print(python_code)
            elif mode == 'both':
                # No modo "all", exibe o código transpilado
                if not args.verbose:
                    print("=" * 60)
                    print("CODIGO PYTHON TRANSPILADO")
                    print("=" * 60)
                print()
                print(python_code)
                if not args.verbose:
                    print()
                    print("=" * 60)
            elif args.verbose:
                print(f"Codigo Python gerado ({len(python_code)} caracteres)")
    
    if mode in ['interpret', 'both'] and success:
        if mode == 'both':
            if args.verbose:
                print_section("EXECUCAO DO CODIGO")
            else:
                print("\n" + "=" * 60)
                print("EXECUCAO DO CODIGO")
                print("=" * 60)
        
        interpret_success = interpret_code(code, args.verbose)
        if not interpret_success:
            success = False
    
    # Salva em arquivo se solicitado
    if args.output and python_code:
        save_to_file(python_code, args.output, args.verbose)
    
    # Mensagem final apenas se verbose
    if args.verbose:
        print("\n" + "=" * 70)
        if success:
            print("COMPILACAO CONCLUIDA COM SUCESSO!")
        else:
            print("COMPILACAO FALHOU")
        print("=" * 70)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperacao cancelada pelo usuario")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        print("Detalhes tecnicos:")
        traceback.print_exc()
        sys.exit(1)
