import numpy as np


def erosao(matrix, valor):
    
    for a in range(1, len(matrix)-1): #altura
        for l in range(1, len(matrix[a])-1): #largura
            for c in range(len(matrix[a][l])): #cor
                cima = matrix[a-1][l][c]
                meio_esq = matrix[a][l-1][c]
                meio_meio = matrix[a][l][c]
                meio_dire = matrix[a][l+1][c]
                baixo = matrix[a+1][l][c]
                lista = np.sort(np.array([cima,meio_esq,meio_meio,meio_dire,baixo]))
                maior = lista[-1] + valor
                matrix[a-1][l][c] = maior
                matrix[a][l-1][c] = maior
                matrix[a][l][c] = maior
                matrix[a][l+1][c] = maior
                matrix[a+1][l][c] = maior

    return matrix
    