// Algoritmos de Ordenação

// Bubble Sort
function bubbleSort(arr) {
    let n = arr.length;
    let trocas = 0;
    
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                // Troca os elementos
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                trocas++;
            }
        }
    }
    
    console.log("Número de trocas realizadas: " + trocas);
    return arr;
}

// Selection Sort
function selectionSort(arr) {
    let n = arr.length;
    
    for (let i = 0; i < n - 1; i++) {
        let menorIndice = i;
        
        for (let j = i + 1; j < n; j++) {
            if (arr[j] < arr[menorIndice]) {
                menorIndice = j;
            }
        }
        
        if (menorIndice !== i) {
            let temp = arr[i];
            arr[i] = arr[menorIndice];
            arr[menorIndice] = temp;
        }
    }
    
    return arr;
}

// Insertion Sort
function insertionSort(arr) {
    for (let i = 1; i < arr.length; i++) {
        let chave = arr[i];
        let j = i - 1;
        
        while (j >= 0 && arr[j] > chave) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        
        arr[j + 1] = chave;
    }
    
    return arr;
}

// Testando os algoritmos
let arrayOriginal = [64, 34, 25, 12, 22, 11, 90];
console.log("Array original: " + arrayOriginal);

let arrayBubble = [64, 34, 25, 12, 22, 11, 90];
console.log("Bubble Sort: " + bubbleSort(arrayBubble));

let arraySelection = [64, 34, 25, 12, 22, 11, 90];
console.log("Selection Sort: " + selectionSort(arraySelection));

let arrayInsertion = [64, 34, 25, 12, 22, 11, 90];
console.log("Insertion Sort: " + insertionSort(arrayInsertion));

// Função para verificar se array está ordenado
function estaOrdenado(arr) {
    for (let i = 0; i < arr.length - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
    }
    return true;
}

console.log("Array está ordenado? " + estaOrdenado([1, 2, 3, 4, 5]));
console.log("Array está ordenado? " + estaOrdenado([5, 3, 1, 4, 2]));
