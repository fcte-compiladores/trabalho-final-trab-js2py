// Classes e Objetos - Sistema de Gerenciamento

// Simulando uma classe Pessoa
function Pessoa(nome, idade, email) {
    this.nome = nome;
    this.idade = idade;
    this.email = email;
}

// Métodos para a "classe" Pessoa
function pessoaToString(pessoa) {
    return "Nome: " + pessoa.nome + ", Idade: " + pessoa.idade + ", Email: " + pessoa.email;
}

function pessoaAniversario(pessoa) {
    pessoa.idade++;
    console.log(pessoa.nome + " fez aniversário! Nova idade: " + pessoa.idade);
}

// Simulando uma classe Conta Bancária
function ContaBancaria(titular, saldoInicial) {
    this.titular = titular;
    this.saldo = saldoInicial || 0;
    this.historico = [];
}

function contaDepositar(conta, valor) {
    if (valor > 0) {
        conta.saldo += valor;
        conta.historico.push("Depósito: +" + valor);
        console.log("Depósito de " + valor + " realizado. Saldo atual: " + conta.saldo);
        return true;
    } else {
        console.log("Valor de depósito deve ser positivo");
        return false;
    }
}

function contaSacar(conta, valor) {
    if (valor > 0 && valor <= conta.saldo) {
        conta.saldo -= valor;
        conta.historico.push("Saque: -" + valor);
        console.log("Saque de " + valor + " realizado. Saldo atual: " + conta.saldo);
        return true;
    } else {
        console.log("Saque inválido. Saldo insuficiente ou valor inválido");
        return false;
    }
}

function contaExibirExtrato(conta) {
    console.log("=== EXTRATO BANCÁRIO ===");
    console.log("Titular: " + conta.titular);
    console.log("Saldo atual: " + conta.saldo);
    console.log("Histórico de transações:");
    
    for (let i = 0; i < conta.historico.length; i++) {
        console.log("- " + conta.historico[i]);
    }
    
    console.log("========================");
}

// Simulando herança - Conta Poupança
function ContaPoupanca(titular, saldoInicial, taxaJuros) {
    ContaBancaria.call(this, titular, saldoInicial);
    this.taxaJuros = taxaJuros || 0.05;
}

function poupancaCalcularJuros(conta) {
    let juros = conta.saldo * conta.taxaJuros;
    conta.saldo += juros;
    conta.historico.push("Juros: +" + juros.toFixed(2));
    console.log("Juros calculados: " + juros.toFixed(2) + ". Novo saldo: " + conta.saldo.toFixed(2));
}

// Sistema de Biblioteca
function Livro(titulo, autor, isbn, disponivel) {
    this.titulo = titulo;
    this.autor = autor;
    this.isbn = isbn;
    this.disponivel = disponivel !== false; // Default true
}

function Biblioteca() {
    this.livros = [];
    this.emprestimos = [];
}

function bibliotecaAdicionarLivro(biblioteca, livro) {
    biblioteca.livros.push(livro);
    console.log("Livro '" + livro.titulo + "' adicionado à biblioteca");
}

function bibliotecaEmprestarLivro(biblioteca, isbn, usuario) {
    for (let i = 0; i < biblioteca.livros.length; i++) {
        let livro = biblioteca.livros[i];
        if (livro.isbn === isbn) {
            if (livro.disponivel) {
                livro.disponivel = false;
                let emprestimo = {
                    livro: livro,
                    usuario: usuario,
                    dataEmprestimo: "2025-01-19"
                };
                biblioteca.emprestimos.push(emprestimo);
                console.log("Livro '" + livro.titulo + "' emprestado para " + usuario);
                return true;
            } else {
                console.log("Livro não está disponível");
                return false;
            }
        }
    }
    console.log("Livro não encontrado");
    return false;
}

function bibliotecaDevolverLivro(biblioteca, isbn) {
    for (let i = 0; i < biblioteca.emprestimos.length; i++) {
        let emprestimo = biblioteca.emprestimos[i];
        if (emprestimo.livro.isbn === isbn) {
            emprestimo.livro.disponivel = true;
            console.log("Livro '" + emprestimo.livro.titulo + "' devolvido por " + emprestimo.usuario);
            
            // Remove o empréstimo do array
            for (let j = i; j < biblioteca.emprestimos.length - 1; j++) {
                biblioteca.emprestimos[j] = biblioteca.emprestimos[j + 1];
            }
            biblioteca.emprestimos.length--;
            return true;
        }
    }
    console.log("Empréstimo não encontrado");
    return false;
}

// Testando o sistema
console.log("=== TESTE DO SISTEMA DE PESSOAS ===");
let pessoa1 = new Pessoa("João", 25, "joao@email.com");
let pessoa2 = new Pessoa("Maria", 30, "maria@email.com");

console.log(pessoaToString(pessoa1));
console.log(pessoaToString(pessoa2));

pessoaAniversario(pessoa1);

console.log("=== TESTE DO SISTEMA BANCÁRIO ===");
let conta = new ContaBancaria("João Silva", 1000);
contaDepositar(conta, 500);
contaSacar(conta, 200);
contaSacar(conta, 2000); // Deve falhar
contaExibirExtrato(conta);

console.log("=== TESTE DA CONTA POUPANÇA ===");
let poupanca = new ContaPoupanca("Maria Santos", 2000, 0.1);
contaDepositar(poupanca, 500);
poupancaCalcularJuros(poupanca);
contaExibirExtrato(poupanca);

console.log("=== TESTE DO SISTEMA DE BIBLIOTECA ===");
let biblioteca = new Biblioteca();
let livro1 = new Livro("1984", "George Orwell", "123456", true);
let livro2 = new Livro("Dom Casmurro", "Machado de Assis", "789012", true);

bibliotecaAdicionarLivro(biblioteca, livro1);
bibliotecaAdicionarLivro(biblioteca, livro2);

bibliotecaEmprestarLivro(biblioteca, "123456", "Carlos");
bibliotecaEmprestarLivro(biblioteca, "123456", "Ana"); // Deve falhar
bibliotecaDevolverLivro(biblioteca, "123456");
bibliotecaEmprestarLivro(biblioteca, "123456", "Ana"); // Agora deve funcionar
