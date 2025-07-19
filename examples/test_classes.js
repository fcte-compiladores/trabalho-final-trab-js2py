class Pessoa {
  constructor(nome, idade) {
    console.log("Criando pessoa...");
  }

  falar() {
    console.log("Olá!");
  }

  andar(passos) {
    console.log("Andando...");
  }
}

class Vazia {}

class SoConstructor {
  constructor() {
    console.log("Só constructor");
  }
}

class SoMetodos {
  metodo1() {
    return "teste";
  }

  metodo2(x, y) {
    return x + y;
  }
}
