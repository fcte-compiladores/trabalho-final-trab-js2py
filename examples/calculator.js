// Calculadora Complexa - Operações matemáticas avançadas

// Operações básicas
function somar(a, b) {
    return a + b;
}

function subtrair(a, b) {
    return a - b;
}

function multiplicar(a, b) {
    return a * b;
}

function dividir(a, b) {
    if (b === 0) {
        console.log("Erro: Divisão por zero!");
        return null;
    }
    return a / b;
}

// Operações avançadas
function potencia(base, expoente) {
    let resultado = 1;
    let exp = Math.abs(expoente);
    
    for (let i = 0; i < exp; i++) {
        resultado *= base;
    }
    
    if (expoente < 0) {
        return 1 / resultado;
    }
    
    return resultado;
}

function raizQuadrada(numero) {
    if (numero < 0) {
        console.log("Erro: Não é possível calcular raiz quadrada de número negativo!");
        return null;
    }
    
    if (numero === 0 || numero === 1) {
        return numero;
    }
    
    // Método de Newton-Raphson
    let estimativa = numero / 2;
    let precisao = 0.000001;
    
    while (true) {
        let novaEstimativa = (estimativa + numero / estimativa) / 2;
        
        if (Math.abs(estimativa - novaEstimativa) < precisao) {
            return novaEstimativa;
        }
        
        estimativa = novaEstimativa;
    }
}

// Função para calcular fatorial
function fatorial(n) {
    if (n < 0) {
        console.log("Erro: Fatorial não definido para números negativos!");
        return null;
    }
    
    if (n === 0 || n === 1) {
        return 1;
    }
    
    let resultado = 1;
    for (let i = 2; i <= n; i++) {
        resultado *= i;
    }
    
    return resultado;
}

// Função para calcular combinação (nCr)
function combinacao(n, r) {
    if (r > n || r < 0 || n < 0) {
        console.log("Erro: Valores inválidos para combinação!");
        return null;
    }
    
    return fatorial(n) / (fatorial(r) * fatorial(n - r));
}

// Função para calcular permutação (nPr)
function permutacao(n, r) {
    if (r > n || r < 0 || n < 0) {
        console.log("Erro: Valores inválidos para permutação!");
        return null;
    }
    
    return fatorial(n) / fatorial(n - r);
}

// Funções trigonométricas (aproximação usando série de Taylor)
function seno(x) {
    // Converte para radianos se necessário e normaliza
    let termo = x;
    let soma = termo;
    
    for (let i = 1; i <= 10; i++) {
        termo *= -1 * x * x / ((2 * i) * (2 * i + 1));
        soma += termo;
    }
    
    return soma;
}

function cosseno(x) {
    let termo = 1;
    let soma = termo;
    
    for (let i = 1; i <= 10; i++) {
        termo *= -1 * x * x / ((2 * i - 1) * (2 * i));
        soma += termo;
    }
    
    return soma;
}

// Logaritmo natural (aproximação)
function logaritmoNatural(x) {
    if (x <= 0) {
        console.log("Erro: Logaritmo não definido para números não positivos!");
        return null;
    }
    
    if (x === 1) {
        return 0;
    }
    
    // Usa série de Taylor para ln(1+u) onde u = x-1
    let u = x - 1;
    let termo = u;
    let soma = termo;
    
    for (let n = 2; n <= 50; n++) {
        termo *= -u;
        soma += termo / n;
    }
    
    return soma;
}

// Calculadora de expressões simples
function calcularExpressao(operando1, operador, operando2) {
    switch (operador) {
        case '+':
            return somar(operando1, operando2);
        case '-':
            return subtrair(operando1, operando2);
        case '*':
            return multiplicar(operando1, operando2);
        case '/':
            return dividir(operando1, operando2);
        case '^':
            return potencia(operando1, operando2);
        default:
            console.log("Operador não reconhecido: " + operador);
            return null;
    }
}

// Função para calcular média de um array
function calcularMedia(numeros) {
    if (numeros.length === 0) {
        console.log("Erro: Array vazio!");
        return null;
    }
    
    let soma = 0;
    for (let i = 0; i < numeros.length; i++) {
        soma += numeros[i];
    }
    
    return soma / numeros.length;
}

// Função para calcular desvio padrão
function calcularDesvioPadrao(numeros) {
    let media = calcularMedia(numeros);
    if (media === null) {
        return null;
    }
    
    let somaQuadrados = 0;
    for (let i = 0; i < numeros.length; i++) {
        let diferenca = numeros[i] - media;
        somaQuadrados += diferenca * diferenca;
    }
    
    let variancia = somaQuadrados / numeros.length;
    return raizQuadrada(variancia);
}

// Testando a calculadora
console.log("=== CALCULADORA COMPLEXA ===");

console.log("Operações básicas:");
console.log("10 + 5 = " + somar(10, 5));
console.log("10 - 3 = " + subtrair(10, 3));
console.log("7 * 8 = " + multiplicar(7, 8));
console.log("15 / 3 = " + dividir(15, 3));
console.log("15 / 0 = " + dividir(15, 0));

console.log("Operações avançadas:");
console.log("2^8 = " + potencia(2, 8));
console.log("2^(-3) = " + potencia(2, -3));
console.log("√16 = " + raizQuadrada(16));
console.log("√2 ≈ " + raizQuadrada(2));

console.log("Fatorial e combinatória:");
console.log("5! = " + fatorial(5));
console.log("C(5,2) = " + combinacao(5, 2));
console.log("P(5,2) = " + permutacao(5, 2));

console.log("Funções trigonométricas (radianos):");
console.log("sen(0) ≈ " + seno(0));
console.log("sen(π/6) ≈ " + seno(3.14159 / 6));
console.log("cos(0) ≈ " + cosseno(0));
console.log("cos(π/3) ≈ " + cosseno(3.14159 / 3));

console.log("Logaritmos:");
console.log("ln(1) = " + logaritmoNatural(1));
console.log("ln(e) ≈ " + logaritmoNatural(2.71828));

console.log("Expressões:");
console.log("Calculando 15 + 7 = " + calcularExpressao(15, '+', 7));
console.log("Calculando 20 / 4 = " + calcularExpressao(20, '/', 4));
console.log("Calculando 3^4 = " + calcularExpressao(3, '^', 4));

console.log("Estatística:");
let dados = [2, 4, 6, 8, 10, 12, 14];
console.log("Dados: " + dados);
console.log("Média: " + calcularMedia(dados));
console.log("Desvio padrão: " + calcularDesvioPadrao(dados));
