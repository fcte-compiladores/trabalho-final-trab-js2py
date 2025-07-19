[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Hppw7Zh2)

# Trabalho Final - FCTE: Compilador JS → Python

## 1. 👥 Contribuidores

<div align="center">
  <table>
    <tr>
      <td align="center"><a href="https://github.com/camilascareli"><img style="border-radius: 50%;" src="https://github.com/camilascareli.png" width="100px;" alt=""/><br /><sub><b>221007582</b></sub></a><br /><a href="https://github.com/camilascareli" title="Rocketseat">Camila Careli</a></td>
      <td align="center"><a href="https://github.com/DanielRogs"><img style="border-radius: 50%;" src="https://github.com/DanielRogs.png" width="100px;" alt=""/><br /><sub><b>211061583</b></sub></a><br /><a href="https://github.com/DanielRogs" title="Rocketseat">Daniel Rodrigues</a></td>
      <td align="center"><a href="https://github.com/DaviRogs"><img style="border-radius: 50%;" src="https://github.com/DaviRogs.png" width="100px;" alt=""/><br /><sub><b>211061618</b></sub></a><br /><a href="https://github.com/DaviRogs" title="Rocketseat">Davi Rodrigues</a></td>
      <td align="center"><a href="https://github.com/rodrigoFAmaral"><img style="border-radius: 50%;" src="https://github.com/rodrigoFAmaral.png" width="100px;" alt=""/><br /><sub><b>231011810</b></sub></a><br /><a href="https://github.com/rodrigoFAmaral" title="Rocketseat">Rodrigo Ferreira</a></td>
    </tr>
  </table>
</div>

## 2. ℹ️ Sobre o projeto

Este projeto implementa um **transpilador e interpretador JavaScript → Python**, desenvolvido como trabalho final da disciplina de Compiladores. A ferramenta oferece duas modalidades distintas de processamento de código JavaScript:

### **🔄 Transpilação (JS → Python)**

Converte código JavaScript em código Python semanticamente equivalente, permitindo a execução posterior em ambiente Python.

### **⚡ Interpretação Direta**

Executa código JavaScript diretamente, sem gerar código intermediário, fornecendo resultados imediatos.

---

## **🛠️ Funcionalidades Suportadas**

O compilador implementa suporte completo para os seguintes recursos do JavaScript:

### **Estruturas de Controle:**

- Condicionais: `if/else`, `if/else if/else`
- Loops: `while`, `for`, `for...in`, `for...of`

### **Declarações de Variáveis:**

- `var`, `let`, `const` com diferentes escopos

### **Funções:**

- Funções tradicionais: `function nome() {}`
- Arrow functions: `() => {}`
- Parâmetros, argumentos e valores de retorno

### **Estruturas de Dados:**

- Arrays: `[1, 2, 3]` e métodos como `.push()`, `.pop()`
- Objetos: `{chave: valor}` e acesso por notação de ponto

### **Operadores:**

- Aritméticos: `+`, `-`, `*`, `/`, `%`
- Comparação: `>`, `<`, `>=`, `<=`, `==`, `===`, `!=`, `!==`
- Lógicos: `&&`, `||`, `!`
- Atribuição: `=`, `+=`, `-=`, etc.

### **Programação Orientada a Objetos:**

- Classes e construtores (usando funções construtoras)
- Métodos e propriedades de instância
- Uso de `this` e `new`

---

## **🔀 Processo de Transpilação**

O processo de transpilação JavaScript → Python segue estas etapas:

```
Código JS → [Tokenizer] → [Parser] → [AST] → [Transpiler] → Código Python
```

### **1. Análise Léxica (`lexer/tokenizer.py`)**

- Recebe o código JavaScript como string
- Divide o código em **tokens** (palavras-chave, operadores, literais, identificadores)
- Remove comentários e espaços desnecessários
- Gera uma lista estruturada de tokens

### **2. Análise Sintática (`parser/parser.py`)**

- Consome os tokens gerados pelo tokenizer
- Aplica as regras gramaticais do JavaScript
- Constrói a **Árvore Sintática Abstrata (AST)** usando classes em `ast_nodes/nodes.py`
- Valida a sintaxe e detecta erros estruturais

### **3. Geração de Código (`translator/transpiler.py`)**

- Percorre a AST gerada pelo parser
- Traduz cada nó da árvore para o equivalente em Python
- Gera código Python idiomático e executável
- **Saída:** Código Python pronto para execução

**Comando:** `uv run python mainTr.py arquivo.js`

---

## **⚡ Processo de Interpretação**

O processo de interpretação executa o código JavaScript diretamente:

```
Código JS → [Tokenizer] → [Parser] → [AST] → [Interpreter] → Execução
```

### **1-2. Análise (mesmas etapas da transpilação)**

- Tokenização e parsing idênticos ao processo de transpilação

### **3. Interpretação Direta (`interpreter/interpreter.py`)**

- Executa a AST diretamente sem gerar código intermediário
- Mantém ambiente de execução com variáveis e funções
- Produz saída imediatamente durante a execução
- **Saída:** Resultado da execução do código JavaScript

**Comando:** `uv run python mainIn.py arquivo.js`

---

## **📁 Fluxo de Arquivos no Projeto**

```
arquivo.js (input)
    ↓
lexer/tokenizer.py (tokenização)
    ↓
parser/parser.py (análise sintática + AST)
    ↓
┌─ translator/transpiler.py → arquivo.py (transpilação)
└─ interpreter/interpreter.py → saída direta (interpretação)
```

## 3. ▶️ Execução

### 3.1. Pré-Requisitos:

O compilador atual utiliza a **linguagem Python** para interpretar o JavaScript e convertê-lo ao Python. Por isso, será necessário que você instale-o em sua máquina seguindo as instruções do site oficial da linguagem: [https://www.python.org/downloads/](https://www.python.org/downloads/).

O projeto também utiliza a ferramenta **uv** para gerenciamento de dependências e ambientes virtuais. Para instalar o `uv`, siga as instruções no site oficial: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/) ou execute:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3.2 Como executar o compilador:

#### PASSO 1: Clonar o Repositório

Para rodar o compilador, é necessário possuir o projeto em sua máquina local. Para isso clone o repositório com o comando:

```shell
git clone https://github.com/fcte-compiladores/trabalho-final-trab-js2py.git
```

Após isso, entre no diretório do projeto.

#### PASSO 2: Verificar Pré-requisitos

Verifique se Python e uv estão instalados:

```shell
python3 --version
uv --version
```

#### PASSO 3: Instalar Dependências

Instale as dependências do projeto usando o uv:

```shell
uv sync
```

#### PASSO 4: Executar o compilador

O projeto agora possui um **script principal unificado** que permite escolher entre transpilação, interpretação ou ambos:

##### **🚀 Script Principal (Recomendado)**

```shell
# Apenas transpila (padrão)
python main.py examples/demo_formatacao.js

# Apenas interpreta/executa
python main.py examples/demo_formatacao.js -i

# Executa ambos (transpila e interpreta)
python main.py examples/demo_formatacao.js -a

# Transpila e salva em arquivo
python main.py examples/demo_formatacao.js -t -o saida.py

# Modo verboso com informações detalhadas
python main.py examples/demo_formatacao.js -a -v

# Ajuda com todas as opções
python main.py --help
```

##### **📜 Scripts Individuais (Compatibilidade)**

Para **transpilar** JavaScript para Python:

```shell
uv run mainTr.py examples/helloWord.js
```

Para **interpretar** JavaScript diretamente:

```shell
uv run mainIn.py examples/helloWord.js
```

#### PASSO 5: Executar Testes (Opcional)

Para executar os testes do projeto:

```shell
uv run pytest
```

## 4. ⚙️ Exemplos

O projeto contém uma pasta `examples/` com diversos arquivos JavaScript utilizados para validar as funcionalidades do compilador.

Entre os arquivos disponíveis, destacam-se:

- **helloWord.js**: exemplo básico de "Hello World" com declaração de variáveis e impressão no console.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/helloWord.js

  # Interpretação:
  uv run mainIn.py examples/helloWord.js
  ```

- **classes_e_objetos.js**: implementação de classes usando funções construtoras, métodos e manipulação de objetos.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/classes_e_objetos.js

  # Interpretação:
  uv run mainIn.py examples/classes_e_objetos.js
  ```

- **estrutura_de_controle.js**: demonstra estruturas condicionais (if/else) e loops (while, for) com exemplos práticos.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/estrutura_de_controle.js

  # Interpretação:
  uv run mainIn.py examples/estrutura_de_controle.js
  ```

- **estrutura_de_dados.js**: trabalha com arrays, objetos e manipulação de diferentes tipos de dados.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/estrutura_de_dados.js

  # Interpretação:
  uv run mainIn.py examples/estrutura_de_dados.js
  ```

- **fibonacci.js**: implementação do algoritmo de Fibonacci, demonstrando recursão e loops.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/fibonacci.js

  # Interpretação:
  uv run mainIn.py examples/fibonacci.js
  ```

- **busca_binaria.js**: algoritmo de busca binária para demonstrar estruturas de controle avançadas.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/busca_binaria.js

  # Interpretação:
  uv run mainIn.py examples/busca_binaria.js
  ```

- **recursao.js**: exemplos diversos de funções recursivas e casos base.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/recursao.js

  # Interpretação:
  uv run mainIn.py examples/recursao.js
  ```

- **manipulacao_de_string.js**: operações com strings, concatenação e métodos de texto.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/manipulacao_de_string.js

  # Interpretação:
  uv run mainIn.py examples/manipulacao_de_string.js
  ```

- **sorting.js**: algoritmos de ordenação como bubble sort e quick sort.

  ```bash
  # Transpilação:
  uv run mainTr.py examples/sorting.js

  # Interpretação:
  uv run mainIn.py examples/sorting.js
  ```

Esses exemplos demonstram desde casos simples, como **declarações de variáveis e estruturas condicionais**, até cenários mais avançados, incluindo **algoritmos, recursão e manipulação de estruturas de dados**.

## 5. 📂 Estrutura do código

A organização do projeto segue uma separação clara por responsabilidades, conforme as etapas do processo de compilação (análise léxica, análise sintática, construção da AST e geração de código):

### **Descrição dos módulos principais**

- **lexer/tokenizer.py** → Faz a **análise léxica**, transformando o código JavaScript em uma lista de tokens.
- **parser/parser.py** → Executa a **análise sintática**, interpretando os tokens e gerando a AST.
- **ast_nodes/nodes.py** → Contém as classes que representam nós da AST (como `Program`, `BinaryOp`, `FunctionDeclaration`).
- **translator/transpiler.py** → Responsável pela **tradução da AST** para código Python equivalente.
- **interpreter/interpreter.py** → Executa a **interpretação direta** do código JavaScript.
- **examples/** → Exemplos práticos de códigos JavaScript que podem ser compilados e interpretados.
- **tests/** → Testes automatizados usando pytest para validação do sistema.
- **mainTr.py** → Ponto de entrada para **transpilação**: converte JavaScript para Python.
- **mainIn.py** → Ponto de entrada para **interpretação**: executa JavaScript diretamente.

### **Arquivos de configuração**

- **pyproject.toml** → Configuração do projeto, dependências e ferramentas (pytest, coverage).
- **uv.lock** → Lock file para garantir reprodutibilidade das dependências.
- **.gitignore** → Arquivos e diretórios ignorados pelo Git.

## 6. 📝 Limitações atuais e possíveis melhorias

## 7. 📌 Referências

- [Crafting Interpreters, Robert Nystrom, 2015-2021.](https://craftinginterpreters.com/)
- [Documentação Oficial do Python](https://docs.python.org/3/)
- [Documentação do JavaScript (MDN Web Docs)](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)
- [PEP 8 – Guia de Estilo para Python](https://peps.python.org/pep-0008/)
- [Introdução à Criação de Compiladores (Dragon Book)](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools)
- [Regex em Python](https://docs.python.org/3/library/re.html)
- [Estrutura de um Transpilador (Artigo)](https://dev.to/lydiahallie/javascript-visualized-the-javascript-engine-4cdf)
