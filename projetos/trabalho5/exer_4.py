#!/usr/local/env python
from random import randint, random
from bitstring import BitArray

def dec_bin(ini, fim, indice, binario):
    decimal = 0
    for i in range(ini, fim):
        decimal += binario[i] * 2 ** indice
        indice -= 1
    return decimal

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

def fitness(cromossomo: list) -> float:
    # decodificacao do cromossomo

    x1, x2 = decodifica(cromossomo)

    # aplicar penalidade
    # solucao para nao zerar o fitness
    penalidade = 0
    if x1 == x2: penalidade = 100

    y1 = x1 ** 2 + 2 * x1 - 3
    y2 = x2 ** 2 + 2 * x2 - 3

    return abs(y1) + abs(y2) + penalidade

def torneio(populacao):
    # 1 passo pegar o tamanho da populacao
    n_populacao = len(populacao)

    # 2 passo realiza o torneio
    pais = []

    # percorre a populacoa
    for i in range(int(len(populacao) / 2)):
        # inicializa os pais
        pai1 = populacao[0][:2]
        pai2 = populacao[0][:2]

        # realiza selecao dos individuos de forma aleatoria para o torneio
        individuo1 = randint(0, n_populacao - 1)
        individuo2 = randint(0, n_populacao - 1)
        individuo3 = randint(0, n_populacao - 1)
        individuo4 = randint(0, n_populacao - 1)

        # caso o fitnes do individuo 1 seja menor que o fitnes do individuo 2
        if populacao[individuo1][1] < populacao[individuo2][1]:
            pai1 = populacao[individuo1]
        else:
            pai1 = populacao[individuo2]

        # caso o fitness do individuo 3 seja menor que o individuo 4
        if populacao[individuo3][1] < populacao[individuo4][1]:
            pai2 = populacao[individuo3]
        else:
            pai2 = populacao[individuo4]

        pais.append([pai1, pai2])

    return pais

def roleta(populacao):
    # 1. Calcula o total do fitness de todos os cromossomos
    total = 1
    for individuo in populacao:
        total += individuo[1]

    # print(f'total: {total}')
    # print('total: {0}'.format(total)) # equivalente

    # 2. Calcula as porcentagens
    #    print('Calculando as porcentagens: ')
    for individuo in populacao:
        individuo.append(individuo[1] / total)
    # print(individuo)

    # 3. Calcula as porcentagens acumuladas

    anterior = 0
    for individuo in populacao:
        acumulado = anterior + individuo[2]
        individuo.append(acumulado)

        anterior = acumulado

    # 4. Gerar os n pares de pais
    pais = []
    for i in range(int(len(populacao) / 2)):
        roleta1 = random()
        roleta2 = random()

        pai1 = populacao[0][:2]
        pai2 = populacao[0][:2]

        # TODO: Verificar pq a roleta esta quebrando
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

# crossover com dois pontos de corte
def crossover_dois_pontos(pais, taxa_mutacao):
    filhos = []

    for par in pais:
        # Extrai os dois pais da lista
        pai1 = par[0][0]
        pai2 = par[1][0]

        # Listas para armazenar os meios
        meio1 = []
        meio2 = []

        # Tag para controlar se achou os cortes ideais
        classificou_cortes = False

        # Sorteia o ponto de corte
        corte_1 = None
        corte_2 = None

        # Sorteia os pontos de corte 1 e 2
        while(classificou_cortes == False):
            corte_1 = randint(0, len(pai1) - 1)
            corte_2 = randint(0, len(pai2) - 1)

            # garante que o corte nao esteja na primeira posicao, nem na ultrima posicao e que o corte_1 seja menor que o corte_2
            if corte_1 > 0 and corte_1 < int(len(pai1) - 1) and corte_2 > 0 and corte_2 < int(len(pai1) - 1) and corte_1 != corte_2 and corte_1 < corte_2:
                classificou_cortes = True

        # Realiza o crossover
        if corte_1 < corte_2:
            # adiciona o meio na lista de meios
            for i in range(corte_1, corte_2):
                meio1.append(pai1[i])
                meio2.append(pai2[i])

            # realiza o cross over
            filho1 = pai1[:corte_1] + meio2 + pai1[corte_2:]
            filho2 = pai2[:corte_1] + meio1 + pai2[corte_2:]

        """
        else:
            print('else')
            for i in range(corte_2, corte_1):
                meio1.append(pai1[i])
                meio2.append(pai2[i])

            filho1 = pai1[:corte_1] + meio2 + pai1[corte_2:]
            filho2 = pai2[:corte_1] + meio1 + pai2[corte_2:]
        """

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

        indice_x1 = len(nova_populacao[0][0][1:8]) - 1
        indice_x2 = len(nova_populacao[0][0][9:16]) - 1

        x1 = dec_bin(1, len(nova_populacao[0][0][1:8]), indice_x1, nova_populacao[0][0])
        x2 = dec_bin(9, len(nova_populacao[0][0]), indice_x2, nova_populacao[0][0])

        if nova_populacao[0][0][0] == 1:
            x1 = x1 * (-1)
        if nova_populacao[0][0][8] == 1:
            x2 = x2 * (-1)
        print(f'X1 = {x1} X2 = {x2}')

        # Selecao dos pais
        #pais = roleta(nova_populacao) # metodo por roleta
        pais = torneio(nova_populacao) # metodo por torneio, testado, resultado bate com a roleta

        # Recomacao (crossover) e mutacao
        #filhos = crossover(pais, taxa_mutacao)
        filhos = crossover_dois_pontos(pais, taxa_mutacao)

        nova_populacao += filhos
        nova_populacao.sort(key=lambda individuo: individuo[1], reverse=False)

        # Selecao dos sobreviventes
        nova_populacao = elitismo(nova_populacao, tam_populacao)

        # passa para geracao seguinte
        geracao += 1

        # Retorna a melhor solucao


def main():
    # ----------------------------------
    # Configuracao dos parametros do AG

    # Numero de alelos do cromossomo
    TAM_CROMOSSOMO = 16

    # Tamanho da populacao
    TAM_POPULACAO = 1000

    # Numero maximo de geracoes
    MAX_GERACOES = 10

    # Taxa de Mutacao
    TAXA_MUTACAO = 0.1  # 1%

    # Execucao do algoritmo
    algoritmo_genetico(TAM_POPULACAO,
                       TAM_CROMOSSOMO,
                       MAX_GERACOES,
                       TAXA_MUTACAO)

    # Imprime a resposta

    pass


if __name__ == '__main__':
    main()