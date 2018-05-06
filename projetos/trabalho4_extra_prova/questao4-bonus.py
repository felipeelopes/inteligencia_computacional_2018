#!/usr/local/env python

import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

# configuracoes globais
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlim3d(-10,30)
ax.set_ylim3d(-10,30)
ax.set_zlim3d(-10,30)
ax.set_xlabel('Temp')
ax.set_ylabel('Umi')
ax.set_zlabel('Vento')


def distancia(x: list, y: list):
    """
        Author: Chaua Queirolo
        Calcula a distancia entre dois pontos
    """
    distancia = 0
    for i in range(0, len(x)):
        distancia += pow(x[i] - y[i], 2)
    return sqrt(distancia)

def plot_centroides(centroides):
    # plotar posicoes centroides gerados
    # consultar cores em https://matplotlib.org/users/colors.html
    cores = ['r', 'g', 'b', 'y', 'c', 'm']

    interator_cor = 0  # interator para as cores

    # plotar centroides
    for row in centroides:
        ax.scatter(row[0], row[1], row[2], marker='*', color=cores[interator_cor])
        interator_cor += 1

def KM(dataset, K) -> list:
    # verificacoes de seguranca
    if K < 2:
        raise ValueError("Numero de clusters 'K' invalido. Informe um numero maior que dois.")

    iter = 0

    # lista que armazena as classes dos elementos
    classes = []

    # lista que armazena os centroides
    centroides = []

    # inicia centroides
    centroides = [[5, 10, 0.1], [25, 20, 1]]
    print("Centroides carregados: ")
    print(centroides)
    #plot_centroides(centroides)

    # carregar dataset na lista pontos
    pontos = []
    for index, linha in dataset.iterrows():
        pontos.append([linha['X'], linha['Y'], linha['Z']])

    print("Pontos Carregados do arquivo: ")
    print(pontos)

    cores = ['r', 'g', 'b', 'y', 'c', 'm']
    # calcular distancias entre o centroid e os pontos
    while True:
        # Para cada elemento do dataset, calcula a distancia com todos os centroids
        for t in pontos:
            distancias = []

            for c in centroides:
                dist = distancia(t, c)
                distancias.append(dist)

            # Verifica em qual classe cada elemento do dataset pertence
            classe = distancias.index(min(distancias))
            classes.append(classe)

        # Recalcula a nova posicao dos centroides
        novos_centroides = []
        for c in range(0, len(centroides)):

            # Inicializa as novas coordenadas do centroide
            centro_massa = [0 for i in centroides[0]]

            # Percorre o dataset pegando somente os pontos do centroide
            num_classes = 0

            for i in range(0, len(pontos)):
                if classes[i] == c:

                    # Calcula o centro de massa para cada atributo
                    for j in range(0, len(pontos[i])):
                        centro_massa[j] += pontos[i][j]

                    # Atualiza o numero de classes
                    num_classes += 1

            # Atualiza as coordenadas dos centroides
            if num_classes == 0:
                novos_centroides.append(centroides[c])
            else:
                novos_centroides.append([x / num_classes for x in centro_massa])

        # Verifica se houve alteracao nos centroides
        diferenca = [distancia(x, y) for x, y in zip(centroides, novos_centroides)]

        # Condicao de parada
        if all(v == 0 for v in diferenca):
            print("Novos Centroids: ")
            print(novos_centroides)

            # plotar grafico com os elementos separados
            for index, linha in enumerate(pontos):
                print("Index: {} X={} Y={} Z={}".format(index, linha[0], linha[1], linha[2]))
                ax.scatter(linha[0], linha[1], linha[2], c=cores[classes[index]], marker='.')

            # plotar centroids
            plot_centroides(novos_centroides)

            # mostrar grafico
            plt.show()
            break

        # Atualiza as variaveis
        centroides = novos_centroides
        iter += 1

        print("Classes: ")
        print(classes)

    return classes

# main
if __name__ == '__main__':
    data = pd.read_csv('data/dataset_prova.csv', sep=';', dtype='float')
    KM(data, 2)