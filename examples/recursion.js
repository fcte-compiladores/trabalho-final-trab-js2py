// Fatorial - Exemplo de recursão
function fatorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * fatorial(n - 1);
}

// Função recursiva para calcular potência
function potencia(base, expoente) {
    if (expoente === 0) {
        return 1;
    }
    if (expoente === 1) {
        return base;
    }
    return base * potencia(base, expoente - 1);
}

// // Função recursiva para inverter string
function inverterString(str) {
    if (str === "") {
        return "";
    }
    return inverterString(str.substr(1)) + str.charAt(0);
}

// // Testando as funções
console.log("Fatorial de 5: " + fatorial(5));
console.log("Fatorial de 0: " + fatorial(0));
console.log("Fatorial de 7: " + fatorial(7));

console.log("2^5 = " + potencia(2, 5));
console.log("3^4 = " + potencia(3, 4));

console.log("Invertendo 'hello': " + inverterString("hello"));
console.log("Invertendo 'recursao': " + inverterString("recursao"));
