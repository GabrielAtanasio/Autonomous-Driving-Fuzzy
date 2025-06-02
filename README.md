# Sistema de Direção Autônoma com Lógica Fuzzy 🚗💨

## Descrição

Este projeto implementa um sistema de controle de direção autônoma utilizando lógica fuzzy. O sistema ajusta a velocidade do veículo e o ângulo de direção com base em sensores de distância para obstáculos à frente e a velocidade atual do veículo. O objetivo é garantir uma condução segura e eficiente, adaptando-se dinamicamente às condições da via e aos obstáculos.

## Componentes do Sistema de Lógica Fuzzy

### 1. Variáveis Linguísticas e Funções de Pertinência

#### Entradas:

* **Distância para o obstáculo (metros)**
    * Universo de Discurso: [0, 20] metros
    * Função de Pertinência: Trapezoidal
    * Termos Linguísticos:
        * `Muito Perto`: Trapmf [0, 0, 1, 2]
        * `Moderada`: Trapmf [1, 2, 5, 6]
        * `Distante`: Trapmf [5, 6, 20, 20]

* **Velocidade atual do veículo (km/h)**
    * Universo de Discurso: [0, 100] km/h
    * Função de Pertinência: Trapezoidal
    * Termos Linguísticos:
        * `Baixa`: Trapmf [0, 0, 10, 20]
        * `Média`: Trapmf [10, 20, 40, 50]
        * `Alta`: Trapmf [40, 50, 100, 100]

#### Saídas:

* **Velocidade ajustada do veículo (km/h)**
    * Universo de Discurso: [0, 60] km/h
    * Função de Pertinência: Triangular
    * Termos Linguísticos:
        * `Baixa`: Trimf [0, 0, 10] (Desacelerar/Parar)
        * `Média`: Trimf [10, 25, 40] (Manter velocidade moderada)
        * `Alta`: Trimf [40, 60, 60] (Acelerar)

* **Direção do veículo (graus)**
    * Universo de Discurso: [-45, 45] graus
    * Função de Pertinência: Triangular
    * Termos Linguísticos:
        * `Esquerda`: Trimf [-45, -30, 0]
        * `Reto`: Trimf [-15, 0, 15]
        * `Direita`: Trimf [0, 30, 45]

### 2. Regras Fuzzy

A base de regras define como as saídas são inferidas a partir das entradas:

1.  **Regra 1:** Se a Distância é `Muito Perto` E a Velocidade Atual é `Alta`, Então a Velocidade Ajustada é `Baixa`.
2.  **Regra 2:** Se a Distância é `Moderada` E a Velocidade Atual é `Média`, Então a Velocidade Ajustada é `Média`.
3.  **Regra 3:** Se a Distância é `Distante` E a Velocidade Atual é `Baixa`, Então a Velocidade Ajustada é `Média`.
4.  **Regra 4:** Se a Distância é `Muito Perto` E a Velocidade Atual é `Baixa`, Então a Velocidade Ajustada é `Baixa`.
5.  **Regra 5:** Se a Distância é `Moderada` E a Velocidade Atual é `Alta`, Então a Velocidade Ajustada é `Média`.
6.  **Regra 6:** Se a Distância é `Moderada`, Então a Direção do Veículo é `Reta`.
7.  **Regra 7:** Se a Distância é `Muito Perto`, Então a Direção do Veículo é `Reta` (para evitar colisão iminente).
8.  **Regra 8:** Se a Distância é `Moderada` E a Velocidade Atual é `Baixa`, Então a Direção do Veículo deve ser `Esquerda` ou `Direita` (dependendo da posição do obstáculo).
    * *Nota sobre a Regra 8:* Esta regra, como formulada, introduz uma ambiguidade ou a necessidade de uma entrada sensorial adicional (posição do obstáculo) para uma decisão determinística. Em implementações, pode ser dividida em duas regras (uma para Esquerda, outra para Direita com a mesma premissa) ou exigir um sensor adicional.

### 3. Processos da Lógica Fuzzy

* **Fuzzificação:** Converte as entradas nítidas (crisp) em graus de pertinência para cada termo linguístico.
* **Inferência:** Aplica as regras fuzzy usando os graus de pertinência das entradas para determinar a ativação (força) de cada regra. O operador `AND` é tipicamente implementado como `MIN`.
* **Agregação:** Combina as saídas de todas as regras ativadas para cada variável de saída, formando um conjunto fuzzy agregado. O operador `OR` (entre regras que levam à mesma consequência ou na agregação) é tipicamente `MAX`.
* **Defuzzificação:** Converte o conjunto fuzzy agregado em um valor de saída nítido. O método do Centro de Gravidade (Centroid) é comumente utilizado.

## Implementação (Exemplo com Python e scikit-fuzzy)

O sistema pode ser implementado utilizando Python com a biblioteca `scikit-fuzzy`.

### Requisitos:

* Python 3.x
* NumPy
* scikit-fuzzy
* Matplotlib (opcional, para visualização)

Você pode instalar as bibliotecas necessárias usando pip:
```bash
pip install numpy scikit-fuzzy matplotlib
