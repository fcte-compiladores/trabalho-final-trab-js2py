[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Hppw7Zh2)

# Trabalho Final - FCTE: Transpilador JS → Python

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
Este projeto implementa um transpilador que converte código JavaScript para Python, contemplando análise léxica, análise sintática, geração de AST e geração de código Python. Ele suporta:
- Estruturas: if/else, while, for...in, for...of
- Declarações: var, let, const
- Funções tradicionais e arrow functions
- Objetos, arrays e métodos
- Operadores lógicos (&&, ||) e comparativos (>, <, ==, ===, etc.)

## 3. ▶️ Execução
### 3.1. Pré-Requisitos:

O compilador atual utiliza a **linguagem Python** para interpretar o JavaScript e convertê-lo ao Python. Por isso, será necessário que você instale-o em sua máquina seguindo as instruções do site oficial da linguagem: [https://www.python.org/downloads/](https://www.python.org/downloads/).

### 3.2 Como executar o compilador:

#### PASSO 1: Clonar o Repositório
Para rodar o compilador, é necessário possuir o projeto em sua máquina local. Para isso clone o repositório com o comando:

```shell
git clone https://github.com/fcte-compiladores/trabalho-final-trab-js2py.git
```

Após isso, entre no diretório do projeto.

#### PASSO 2: Verificar 3.1
```shell
python3 --version
```

#### PASSO 3: Executar o compilador
Dentro da pasta do projeto, utilize um dos arquivos já existentes na pasta `examples/` (por exemplo: `example.js`). Comando:

```shell
python3 main.py examples/example.js
```

## 4. ⚙️ Exemplos
O projeto contém uma pasta `examples/` com diversos arquivos JavaScript utilizados para validar as funcionalidades do compilador. Os exemplos abrangem diferentes níveis de complexidade e cobrem vários recursos da linguagem, garantindo a demonstração prática das capacidades do transpilador.  

Entre os arquivos disponíveis, destacam-se:
- **example.js**: exemplo básico que demonstra operações simples e impressão no console.
- **test_classes.js / test_advanced_classes.js**: exemplos com definição de classes, métodos e construtores.
- **test_simple_class.js / test_this.js**: uso do `this` e atributos de instância.
- **test_method_call.js**: chamadas de métodos de objetos.
- **test_comments.js**: validação do tratamento de comentários.
- **test_new.js**: uso do operador `new` para instanciar objetos.
- **test_encoding.js**: manipulação de strings e codificação.
- **test_complete.js**: script mais complexo, combinando múltiplas estruturas e funcionalidades.

Esses exemplos demonstram desde casos simples, como **declarações de variáveis e estruturas condicionais**, até cenários mais avançados, incluindo **programação orientada a objetos e manipulação de dados**.


## 5. 📂 Estrutura do código
A organização do projeto segue uma separação clara por responsabilidades, conforme as etapas do processo de compilação (análise léxica, análise sintática, construção da AST e geração de código):

### **Descrição dos módulos principais**
- **lexer/tokenizer.py** → Faz a **análise léxica**, transformando o código JavaScript em uma lista de tokens.
- **parser/parser.py** → Executa a **análise sintática**, interpretando os tokens e gerando a AST.
- **ast_nodes/nodes.py** → Contém as classes que representam nós da AST (como `Program`, `BinaryOp`, `FunctionDeclaration`).
- **translator/transpiler.py** → Responsável pela **tradução da AST** para código Python equivalente.
- **examples/** → Exemplos práticos de códigos JavaScript que podem ser compilados.
- **main.py** → Ponto de entrada do sistema; orquestra todas as etapas: tokenização, parsing e geração de código.


## 6. 📝 Limitações atuais e possíveis melhorias


## 7. 📌 Referências
* [Crafting Interpreters, Robert Nystrom, 2015-2021.](https://craftinginterpreters.com/)
* [Documentação Oficial do Python](https://docs.python.org/3/)
* [Documentação do JavaScript (MDN Web Docs)](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)
* [PEP 8 – Guia de Estilo para Python](https://peps.python.org/pep-0008/)
* [Introdução à Criação de Compiladores (Dragon Book)](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools)
* [Regex em Python](https://docs.python.org/3/library/re.html)
* [Estrutura de um Transpilador (Artigo)](https://dev.to/lydiahallie/javascript-visualized-the-javascript-engine-4cdf)



