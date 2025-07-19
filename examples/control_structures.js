// Estruturas de Controle - If/Else, While, For

// Exemplo com if/else aninhados
function classificarIdade(idade) {
    if (idade < 0) {
        return "Idade inválida";
    } else if (idade < 13) {
        return "Criança";
    } else if (idade < 18) {
        return "Adolescente";
    } else if (idade < 60) {
        return "Adulto";
    } else {
        return "Idoso";
    }
}

// Exemplo com switch simulado usando if/else
function obterDiaSemana(numero) {
    if (numero === 1) {
        return "Domingo";
    } else if (numero === 2) {
        return "Segunda-feira";
    } else if (numero === 3) {
        return "Terça-feira";
    } else if (numero === 4) {
        return "Quarta-feira";
    } else if (numero === 5) {
        return "Quinta-feira";
    } else if (numero === 6) {
        return "Sexta-feira";
    } else if (numero === 7) {
        return "Sábado";
    } else {
        return "Dia inválido";
    }
}

// Loops - While
function contarAte(limite) {
    let contador = 1;
    console.log("Contando até " + limite + " com while:");
    
    while (contador <= limite) {
        console.log(contador);
        contador++;
    }
}

// Loops - For
function tabuada(numero) {
    console.log("Tabuada do " + numero + ":");
    
    for (let i = 1; i <= 10; i++) {
        console.log(numero + " x " + i + " = " + (numero * i));
    }
}

// Loop aninhado - Matriz
function imprimirMatriz() {
    console.log("Matriz 3x3:");
    
    for (let i = 1; i <= 3; i++) {
        let linha = "";
        for (let j = 1; j <= 3; j++) {
            linha += (i * j) + " ";
        }
        console.log(linha);
    }
}

// Verificação de número primo
function ehPrimo(numero) {
    if (numero <= 1) {
        return false;
    }
    
    if (numero === 2) {
        return true;
    }
    
    if (numero % 2 === 0) {
        return false;
    }
    
    for (let i = 3; i * i <= numero; i += 2) {
        if (numero % i === 0) {
            return false;
        }
    }
    
    return true;
}

// Função para encontrar números primos até N
function encontrarPrimos(limite) {
    console.log("Números primos até " + limite + ":");
    
    for (let i = 2; i <= limite; i++) {
        if (ehPrimo(i)) {
            console.log(i);
        }
    }
}

// Testando as funções
console.log("Classificação de idades:");
console.log("5 anos: " + classificarIdade(5));
console.log("15 anos: " + classificarIdade(15));
console.log("25 anos: " + classificarIdade(25));
console.log("65 anos: " + classificarIdade(65));

console.log("Dias da semana:");
console.log("Dia 1: " + obterDiaSemana(1));
console.log("Dia 5: " + obterDiaSemana(5));
console.log("Dia 8: " + obterDiaSemana(8));

contarAte(5);
tabuada(7);
imprimirMatriz();

console.log("Verificação de números primos:");
console.log("17 é primo? " + ehPrimo(17));
console.log("15 é primo? " + ehPrimo(15));

encontrarPrimos(20);
