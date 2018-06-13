#!/usr/local/env python

from random import randint, random


# Cromossomo: usado para modelar a solucao
#           - eh a solucao do problema
#           - cromossomo = solucao = individuo


# Modelagem do problema
# Problema: maximizar o numero de 1s no cromossomo
#   - Precisa definir a funcao de fitness
#   - Precisa definir o fenotipo do cromossomo

def fitness(cromossomo: list) -> float:
    # Funcao de fitness: avalia um cromossomo
    # - Deve ser capaz de avaliar se um cromossomo eh melhor que outro
    # - Avalia se a solucao eh boa ou ruim

    # decodificacao do cromossomo
    indice = len(cromossomo) - 1
    x = 0
    for i in range(len(cromossomo)):
        x += cromossomo[i] * 2 ** indice
        indice -= 1

    # Para o problema de achar o maximo da funcao
    # return -x ** 2 + 2 * x + 3
    return -2.2 * x ** 2 + 8.6 * x + 1

def torneio(populacao, k_inidividuos):
    pass

def aleatorio(populacao):
    pass

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

    # print(f'total: {total}')
    # print('total: {0}'.format(total)) # equivalente

    # 2. Calcula as porcentagens
    #    print('Calculando as porcentagens: ')
    for individuo in populacao:
        individuo.append(individuo[1] / total)
    # print(individuo)

    # 3. Calcula as porcentagens acumuladas
    #    print('Calculando as porcentagens acumuladas: ')

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

        # TODO: Verificar pq a roleta esta quebrando
        for individuo in populacao:
            # print(f'1: {roleta1} - {individuo[3]}')
            if roleta1 <= individuo[3]:
                pai1 = individuo[:2]
                break

        for individuo in populacao:
            # print(f'2: {roleta2} - {individuo[3]} - {populacao}')
            if roleta2 <= individuo[3]:
                pai2 = individuo[:2]
                break

                # TODO: Corrigir a selecao de 2 pais iguais
                #        print(f'>>1 {pai1} ')
                #        print(f'>>2 {pai2} ')
        pais.append([pai1, pai2])

    # print('Lista de pais:')
    #    for individuo in pais:
    #        print(f'{individuo[0][0]} - {individuo[1][0]}')

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
                #                print(f'Sofreu mutacao! {probabilidade}')
                #                print(f'antes:  {filho1}')
                filho1[i] = int(not filho1[i])
                #                print(f'depois: {filho1}')

        for i in range(0, len(filho2)):
            probabilidade = random()

            if probabilidade < taxa_mutacao:
                #                print(f'Sofreu mutacao! {probabilidade}')
                #                print(f'antes:  {filho2}')
                filho2[i] = int(not filho2[i])
                #                print(f'depois: {filho2}')

        # Salva os filhos gerados
        filhos.append([filho1, fitness(filho1)])
        filhos.append([filho2, fitness(filho2)])

        #   print('Filhos gerados: ')
        #   for individuo in filhos:
        #       print(f'{individuo[0]} => {individuo[1]}')

    return filhos


def elitismo(populacao, tam_populacao):
    # Ordena pelo fitness
    populacao.sort(key=lambda individuo: individuo[1], reverse=True)

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
        nova_populacao.sort(key=lambda individuo: individuo[1], reverse=True)
        print(f'{nova_populacao[0][0]} => {nova_populacao[0][1]}')

        #for individuo in nova_populacao:
        #    print(f'{individuo[0]} => {individuo[1]}')

        # Selecao dos pais
        pais = roleta(nova_populacao)

        # Recombinacao (crossover) e mutacao
        filhos = crossover(pais, taxa_mutacao)

        nova_populacao += filhos
        nova_populacao.sort(key=lambda individuo: individuo[1], reverse=True)

        #        print('Populacao total')
        #        for individuo in nova_populacao:
        #            print(f'{individuo[0]} => {individuo[1]}')

        # Selecao dos sobreviventes
        nova_populacao = elitismo(nova_populacao, tam_populacao)

        #        print('Populacao sobrevivente')
        #        for individuo in nova_populacao:
        #            print(f'{individuo[0]} => {individuo[1]}')

        # passa para geracao seguinte
        geracao += 1

        # Retorna a melhor solucao


def main():
    # ----------------------------------
    # Configuracao dos parametros do AG

    # Numero de alelos do cromossomo
    TAM_CROMOSSOMO = 5

    # Tamanho da populacao
    TAM_POPULACAO = 10

    # Numero maximo de geracoes
    MAX_GERACOES = 20

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