// Algoritmos de Busca

// Busca Linear
function buscaLinear(arr, elemento) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === elemento) {
            return i;
        }
    }
    return -1;
}

// Busca Binária (array deve estar ordenado)
function buscaBinaria(arr, elemento) {
    let inicio = 0;
    let fim = arr.length - 1;
    
    while (inicio <= fim) {
        let meio = Math.floor((inicio + fim) / 2);
        
        if (arr[meio] === elemento) {
            return meio;
        }
        
        if (arr[meio] < elemento) {
            inicio = meio + 1;
        } else {
            fim = meio - 1;
        }
    }
    
    return -1;
}

// Busca Binária Recursiva
function buscaBinariaRecursiva(arr, elemento, inicio, fim) {
    if (inicio > fim) {
        return -1;
    }
    
    let meio = Math.floor((inicio + fim) / 2);
    
    if (arr[meio] === elemento) {
        return meio;
    }
    
    if (arr[meio] < elemento) {
        return buscaBinariaRecursiva(arr, elemento, meio + 1, fim);
    } else {
        return buscaBinariaRecursiva(arr, elemento, inicio, meio - 1);
    }
}

// Função para encontrar primeira ocorrência em array ordenado
function encontrarPrimeiraOcorrencia(arr, elemento) {
    let resultado = buscaBinaria(arr, elemento);
    
    if (resultado === -1) {
        return -1;
    }
    
    // Encontra a primeira ocorrência
    while (resultado > 0 && arr[resultado - 1] === elemento) {
        resultado--;
    }
    
    return resultado;
}

// Testando os algoritmos
let arrayOrdenado = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
let arrayComDuplicatas = [1, 2, 2, 2, 3, 4, 5, 5, 6];

console.log("Array ordenado: " + arrayOrdenado);

let elementoProcurado = 7;
console.log("Procurando elemento " + elementoProcurado + ":");

let resultadoLinear = buscaLinear(arrayOrdenado, elementoProcurado);
console.log("Busca Linear: posição " + resultadoLinear);

let resultadoBinaria = buscaBinaria(arrayOrdenado, elementoProcurado);
console.log("Busca Binária: posição " + resultadoBinaria);

let resultadoRecursiva = buscaBinariaRecursiva(arrayOrdenado, elementoProcurado, 0, arrayOrdenado.length - 1);
console.log("Busca Binária Recursiva: posição " + resultadoRecursiva);

// Testando elemento que não existe
let elementoInexistente = 8;
console.log("Procurando elemento inexistente " + elementoInexistente + ":");
console.log("Resultado: " + buscaBinaria(arrayOrdenado, elementoInexistente));

// Testando primeira ocorrência
console.log("Array com duplicatas: " + arrayComDuplicatas);
console.log("Primeira ocorrência de 2: posição " + encontrarPrimeiraOcorrencia(arrayComDuplicatas, 2));
console.log("Primeira ocorrência de 5: posição " + encontrarPrimeiraOcorrencia(arrayComDuplicatas, 5));
