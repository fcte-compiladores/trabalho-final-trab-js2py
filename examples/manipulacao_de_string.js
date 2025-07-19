// Manipulação de Strings

// Função para contar caracteres
function contarCaracteres(str, char) {
    let contador = 0;
    for (let i = 0; i < str.length; i++) {
        if (str.charAt(i) === char) {
            contador++;
        }
    }
    return contador;
}

// Função para verificar se é palíndromo
function ehPalindromo(str) {
    let strLimpa = str.toLowerCase();
    let inicio = 0;
    let fim = strLimpa.length - 1;
    
    while (inicio < fim) {
        if (strLimpa.charAt(inicio) !== strLimpa.charAt(fim)) {
            return false;
        }
        inicio++;
        fim--;
    }
    
    return true;
}

// Função para contar palavras
function contarPalavras(str) {
    let palavras = 0;
    let dentroPalavra = false;
    
    for (let i = 0; i < str.length; i++) {
        if (str.charAt(i) !== ' ' && str.charAt(i) !== '\t' && str.charAt(i) !== '\n') {
            if (!dentroPalavra) {
                palavras++;
                dentroPalavra = true;
            }
        } else {
            dentroPalavra = false;
        }
    }
    
    return palavras;
}

// Função para remover espaços extras
function removerEspacosExtras(str) {
    let resultado = "";
    let espacoAnterior = true;
    
    for (let i = 0; i < str.length; i++) {
        if (str.charAt(i) === ' ') {
            if (!espacoAnterior) {
                resultado += ' ';
                espacoAnterior = true;
            }
        } else {
            resultado += str.charAt(i);
            espacoAnterior = false;
        }
    }
    
    return resultado;
}

// Função para capitalizar primeira letra de cada palavra
function capitalizarPalavras(str) {
    let resultado = "";
    let proximaMaiuscula = true;
    
    for (let i = 0; i < str.length; i++) {
        let char = str.charAt(i);
        
        if (char === ' ') {
            resultado += char;
            proximaMaiuscula = true;
        } else if (proximaMaiuscula) {
            resultado += char.toUpperCase();
            proximaMaiuscula = false;
        } else {
            resultado += char.toLowerCase();
        }
    }
    
    return resultado;
}

// Testando as funções
let texto = "JavaScript para Python";
console.log("Texto original: '" + texto + "'");
console.log("Contando 'a': " + contarCaracteres(texto, 'a'));
console.log("Contando 'P': " + contarCaracteres(texto, 'P'));

let palindromo1 = "arara";
let palindromo2 = "hello";
console.log("'" + palindromo1 + "' é palíndromo? " + ehPalindromo(palindromo1));
console.log("'" + palindromo2 + "' é palíndromo? " + ehPalindromo(palindromo2));

let frase = "Este é um exemplo de frase com várias palavras";
console.log("Frase: '" + frase + "'");
console.log("Número de palavras: " + contarPalavras(frase));

let textoComEspacos = "  Este   texto  tem    espaços   extras  ";
console.log("Texto com espaços: '" + textoComEspacos + "'");
console.log("Texto limpo: '" + removerEspacosExtras(textoComEspacos) + "'");

let textoParaCapitalizar = "javascript é uma linguagem incrível";
console.log("Texto original: '" + textoParaCapitalizar + "'");
console.log("Capitalizado: '" + capitalizarPalavras(textoParaCapitalizar) + "'");
