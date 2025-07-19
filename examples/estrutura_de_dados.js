// Estruturas de Dados - Arrays e Objetos

// Trabalhando com Arrays
let numeros = [1, 2, 3, 4, 5];
let frutas = ["maçã", "banana", "laranja"];
let misto = [1, "texto", true, 3.14];

console.log("Array de números:");
console.log(numeros);

console.log("Array de frutas:");
console.log(frutas);

// Função para somar elementos de um array
function somarArray(arr) {
    let soma = 0;
    for (let i = 0; i < arr.length; i++) {
        soma += arr[i];
    }
    return soma;
}

// Função para encontrar o maior elemento
function encontrarMaior(arr) {
    let maior = arr[0];
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] > maior) {
            maior = arr[i];
        }
    }
    return maior;
}

console.log("Soma do array: " + somarArray(numeros));
console.log("Maior elemento: " + encontrarMaior(numeros));

// Trabalhando com Objetos
let pessoa = {
    nome: "João",
    idade: 30,
    cidade: "São Paulo"
};

let carro = {
    marca: "Toyota",
    modelo: "Corolla",
    ano: 2020,
    cor: "azul"
};

console.log("Dados da pessoa:");
console.log("Nome: " + pessoa.nome);
console.log("Idade: " + pessoa.idade);
console.log("Cidade: " + pessoa.cidade);

console.log("Dados do carro:");
console.log("Marca: " + carro.marca);
console.log("Modelo: " + carro.modelo);
console.log("Ano: " + carro.ano);

// Array de objetos
let estudantes = [
    { nome: "Ana", nota: 8.5 },
    { nome: "Bruno", nota: 7.2 },
    { nome: "Carlos", nota: 9.1 },
    { nome: "Diana", nota: 6.8 }
];

// Função para calcular média das notas
function calcularMedia(estudantes) {
    let soma = 0;
    for (let i = 0; i < estudantes.length; i++) {
        soma += estudantes[i].nota;
    }
    return soma / estudantes.length;
}

console.log("Média das notas: " + calcularMedia(estudantes));
