#!/usr/local/env python
from random import randint, random
from bitstring import BitArray
import numpy as np

def decodifica(cromossomo):

    # Extrai o sinal
    sinal_x = cromossomo[0]
    sinal_y = cromossomo[8]

    # Extrai o numero e converte para inteiro
    x = BitArray(cromossomo[1:8]).uint
    y = BitArray(cromossomo[9:16]).uint

    # Aplica o sinal no numero
    if sinal_x == 1: x *= -1
    if sinal_y == 1: y *= -1

    return x, y

def dec_bin(ini, fim, indice, binario):
    decimal = 0
    for i in range(ini, fim):
        decimal += binario[i] * 2 ** indice
        indice -= 1
    return decimal

def fitness(cromossomo: list) -> float:
    # Funcao de fitness: avalia um cromossomo
    # - Deve ser capaz de avaliar se um cromossomo eh melhor que outro
    # - Avalia se a solucao eh boa ou ruim

    # decodifica cromossomo
    x, y = decodifica(cromossomo)

    # achar o minimo da funcao
    solucao = x * y * np.sin((y * np.pi) / 4)
    #print(f'Solucao Calculada = {solucao}')

    if (x >= -100 and y >= -100) and (y <= 100 and y <= 100):
        return abs(solucao)
    else:
        return 999999

def roleta(populacao):
    """
    Implementacao do algoritmo da roleta viciada.
    :param populacao: lista com todos os cromossomos
    :return: lista com os pares de pais que vao cruzar entre si
    """

    # 1. Calcula o total do fitness de todos os cromossomos
    total = 0
    for individuo in populacao:
        total += individuo[1]

    # 2. Calcula as porcentagens
    for individuo in populacao:
        individuo.append(individuo[1] / total)
    # print(individuo)

    # 3. Calcula as porcentagens acumuladas
    anterior = 0
    for individuo in populacao:
        acumulado = anterior + individuo[2]
        individuo.append(acumulado)

        anterior = acumulado
    # print(individuo)

    # 4. Gerar os n pares de pais
    pais = []
    for i in range(int(len(populacao) / 2)):
        roleta1 = random()
        roleta2 = random()

        pai1 = populacao[0][:2]
        pai2 = populacao[0][:2]

        for individuo in populacao:
            if roleta1 <= individuo[3]:
                pai1 = individuo[:2]
                break

        for individuo in populacao:
            if roleta2 <= individuo[3]:
                pai2 = individuo[:2]
                break

        pais.append([pai1, pai2])

    return pais

def crossover(pais, taxa_mutacao):
    filhos = []

    for par in pais:
        # Extrai os dois pais da lista
        pai1 = par[0][0]
        pai2 = par[1][0]

        # Sorteia o ponto de corte
        corte = randint(0, len(pai1) - 1)

        # Realiza o crossover
        filho1 = pai1[:corte] + pai2[corte:]
        filho2 = pai2[:corte] + pai1[corte:]

        # Aplica a mutacao
        for i in range(0, len(filho1)):
            probabilidade = random()

            if probabilidade < taxa_mutacao:
                filho1[i] = int(not filho1[i])

        for i in range(0, len(filho2)):
            probabilidade = random()

            if probabilidade < taxa_mutacao:
                filho2[i] = int(not filho2[i])

        # Salva os filhos gerados
        filhos.append([filho1, fitness(filho1)])
        filhos.append([filho2, fitness(filho2)])

    return filhos


def elitismo(populacao, tam_populacao):
    # Ordena pelo fitness
    populacao.sort(key=lambda individuo: individuo[1], reverse=False)

    # Retorna os n primeiros
    return populacao[:tam_populacao]


def algoritmo_genetico(tam_populacao,
                       tam_cromossomo,
                       max_geracoes,
                       taxa_mutacao):
    # Inicializa a populacao
    populacao = [
        [randint(0, 1) for i in range(0, tam_cromossomo)]
        for j in range(0, tam_populacao)
    ]
    print(populacao)

    # Avaliacao dos cromossomos
    nova_populacao = [
        [cromossomo, fitness(cromossomo)]
        for cromossomo in populacao
    ]

    # Geracoes
    geracao = 0

    while geracao < max_geracoes:

        print(f'### GERACAO {geracao} ###')
        nova_populacao.sort(key=lambda individuo: individuo[1], reverse=False)

        print(f'{nova_populacao[0][0]} => {nova_populacao[0][1]}')

        # decodificacao do cromossomo
        indice_x = len(nova_populacao[0][0][1:8]) - 1
        indice_y = len(nova_populacao[0][0][9:16]) - 1

        x = dec_bin(1, len(nova_populacao[0][0][1:8]), indice_x, nova_populacao[0][0])
        y = dec_bin(9, len(nova_populacao[0][0]), indice_y, nova_populacao[0][0])

        if nova_populacao[0][0][0] == 1:
            x = x * (-1)
        if nova_populacao[0][0][8] == 1:
            y = y * (-1)

        print(f'X = {x} y = {y}')

        # Selecao dos pais
        pais = roleta(nova_populacao)

        # Recomacao (crossover) e mutacao
        filhos = crossover(pais, taxa_mutacao)

        nova_populacao += filhos
        nova_populacao.sort(key=lambda individuo: individuo[1], reverse=False)

        # Selecao dos sobreviventes
        nova_populacao = elitismo(nova_populacao, tam_populacao)

        # passa para geracao seguinte
        geracao += 1

    return nova_populacao

def main():
    # ----------------------------------
    # Configuracao dos parametros do AG

    # Numero de alelos do cromossomo
    TAM_CROMOSSOMO = 16

    # Tamanho da populacao
    TAM_POPULACAO = 100

    # Numero maximo de geracoes
    MAX_GERACOES = 10

    # Taxa de Mutacao
    TAXA_MUTACAO = 0.01  # 1%

    # Execucao do algoritmo
    algoritmo_genetico(TAM_POPULACAO,
                       TAM_CROMOSSOMO,
                       MAX_GERACOES,
                       TAXA_MUTACAO)

    # Imprime a resposta

    pass


if __name__ == '__main__':
    main()