from parser.parser import Parser
from interpreter.interpreter import Interpreter 
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python mainIn.py <arquivo_entrada.js>")
        return

    input_file = sys.argv[1]
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    print(f"--- Executando o arquivo: {input_file} ---\n")

    try:
        parser = Parser(code)
        ast = parser.parse_program()

        interpreter = Interpreter(ast)
        interpreter.execute()

        print("\n--- Execução concluída ---")

    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main()