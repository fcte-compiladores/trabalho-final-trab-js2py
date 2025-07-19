// Quick Sort - Algoritmo de ordenação mais elaborado

function quickSort(arr, inicio, fim) {
    if (inicio < fim) {
        let indicePivo = particionar(arr, inicio, fim);
        
        quickSort(arr, inicio, indicePivo - 1);
        quickSort(arr, indicePivo + 1, fim);
    }
    
    return arr;
}

function particionar(arr, inicio, fim) {
    let pivo = arr[fim];
    let i = inicio - 1;
    
    for (let j = inicio; j < fim; j++) {
        if (arr[j] <= pivo) {
            i++;
            trocar(arr, i, j);
        }
    }
    
    trocar(arr, i + 1, fim);
    return i + 1;
}

function trocar(arr, i, j) {
    let temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

// Merge Sort - Outro algoritmo eficiente
function mergeSort(arr) {
    if (arr.length <= 1) {
        return arr;
    }
    
    let meio = Math.floor(arr.length / 2);
    let esquerda = mergeSort(arr.slice(0, meio));
    let direita = mergeSort(arr.slice(meio));
    
    return mesclar(esquerda, direita);
}

function mesclar(esquerda, direita) {
    let resultado = [];
    let i = 0;
    let j = 0;
    
    while (i < esquerda.length && j < direita.length) {
        if (esquerda[i] <= direita[j]) {
            resultado.push(esquerda[i]);
            i++;
        } else {
            resultado.push(direita[j]);
            j++;
        }
    }
    
    while (i < esquerda.length) {
        resultado.push(esquerda[i]);
        i++;
    }
    
    while (j < direita.length) {
        resultado.push(direita[j]);
        j++;
    }
    
    return resultado;
}

// Função para gerar array aleatório
function gerarArrayAleatorio(tamanho, max) {
    let arr = [];
    for (let i = 0; i < tamanho; i++) {
        arr.push(Math.floor(Math.random() * max) + 1);
    }
    return arr;
}

// Função para medir tempo de execução (simulada)
function medirTempo(algoritmo, arr, nome) {
    console.log("Executando " + nome + "...");
    let arrCopia = arr.slice(); // Cria uma cópia
    
    if (nome === "Quick Sort") {
        algoritmo(arrCopia, 0, arrCopia.length - 1);
    } else {
        arrCopia = algoritmo(arrCopia);
    }
    
    console.log(nome + " concluído");
    return arrCopia;
}

// Função para verificar se está ordenado
function verificarOrdenacao(arr) {
    for (let i = 0; i < arr.length - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
    }
    return true;
}

// Testando os algoritmos
let arrayTeste = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42];
console.log("Array original: " + arrayTeste);

// Quick Sort
let arrayQuick = arrayTeste.slice();
let resultadoQuick = medirTempo(quickSort, arrayQuick, "Quick Sort");
console.log("Quick Sort resultado: " + resultadoQuick);
console.log("Quick Sort está ordenado? " + verificarOrdenacao(resultadoQuick));

// Merge Sort
let arrayMerge = arrayTeste.slice();
let resultadoMerge = medirTempo(mergeSort, arrayMerge, "Merge Sort");
console.log("Merge Sort resultado: " + resultadoMerge);
console.log("Merge Sort está ordenado? " + verificarOrdenacao(resultadoMerge));

// Teste com array maior
console.log("Testando com array de 15 elementos aleatórios:");
let arrayGrande = gerarArrayAleatorio(15, 100);
console.log("Array aleatório: " + arrayGrande);

let arrayGrandeQuick = arrayGrande.slice();
quickSort(arrayGrandeQuick, 0, arrayGrandeQuick.length - 1);
console.log("Quick Sort (array grande): " + arrayGrandeQuick);

let arrayGrandeMerge = mergeSort(arrayGrande.slice());
console.log("Merge Sort (array grande): " + arrayGrandeMerge);
