#!/usr/local/env python

from math import sqrt


def calcular_distancia(x: list, y: list):
    """Calcula a distancia entre dois pontos"""
    distancia = 0
    for i in range(0, len(x)):
        distancia += pow(x[i] - y[i], 2)
    return sqrt(distancia)


def kmeans(dataset: list, centroides: list) -> list:
    """Calcula as classes que cada ponto do dataset pertence."""

    iter = 0

    while True:
        print(f'### {iter} ###')
        print(f'centroides: {centroides}')

        classes = []  # classes as quais cada elemento do dataset pertence

        # Para cada elemento do dataset, calcula a distancia com todos os centroids
        for t in dataset:
            distancias = []

            for c in centroides:
                dist = calcular_distancia(t, c)
                distancias.append(dist)

            print(f't{dataset.index(t)}: {distancias}')

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

            for i in range(0, len(dataset)):
                if classes[i] == c:

                    # Calcula o centro de massa para cada atributo
                    for j in range(0, len(dataset[i])):
                        centro_massa[j] += dataset[i][j]

                    # Atualiza o numero de classes
                    num_classes += 1

            # Atualiza as coordenadas dos centroides
            if num_classes == 0:
                novos_centroides.append(centroides[c])
            else:
                novos_centroides.append([x / num_classes for x in centro_massa])

        # Verifica se houve alteracao nos centroides
        diferenca = [calcular_distancia(x, y) for x, y in zip(centroides, novos_centroides)]

        # Condicao de parada
        if all(v == 0 for v in diferenca):
            break

        # Atualiza as variaveis
        centroides = novos_centroides
        iter += 1

    return classes


def main():
    dataset = [
        [10, 20, 1],
        [8, 13, 0],
        [6, 15, 1],
        [5, 11, 1],
        [20, 26, 0],
        [22, 26, 0],
        [23, 27, 1],
        [18, 23, 0]
    ]

    centroides = [
        [5, 10, 0],
        [25, 20, 1]
    ]

    classes = kmeans(dataset, centroides)

    print(dataset, classes)


if __name__ == '__main__':
    main()
