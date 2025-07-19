// Fibonacci - Função recursiva
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Testando a função
console.log("Sequência de Fibonacci:");
for (let i = 0; i < 10; i++) {
    console.log("fibonacci(" + i + ") = " + fibonacci(i));
}

// Versão iterativa para comparação
function fibonacciIterativo(n) {
    if (n <= 1) {
        return n;
    }
    
    let a = 0;
    let b = 1;
    let temp;
    
    for (let i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    
    return b;
}

console.log("Fibonacci iterativo de 10: " + fibonacciIterativo(10));
