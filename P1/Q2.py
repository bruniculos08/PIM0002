# Alunos: Bruno R. dos Santos e Luigi
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
import copy

greenComponent = [(0, -1), (0, 1), (-1, 0), (1, 0)]
redComponentAtBlue = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
redComponentAtGreen = [(1, 0), (-1, 0)]
blueComponentAtRed = [(-1,-1), (-1,1), (1,-1), (1, 1)]
blueComponentAtGreen = [(0, 1), (0, -1)]

def getColor(pixels, line, col):
    if line < 0 or line >= len(pixels):
        return [0, 0, 0]
    if col < 0 or col >= len(pixels[0]):
        return [0, 0, 0]
    return pixels[line][col]

def BayerFilter(pixels):
    height = len(pixels)
    width = len(pixels[0])
    colored_pixels = np.zeros((height, width, 3), dtype=np.uint8)
    # Obs.: a imagem está em BGR.
    for i in range(0, height):
        for j in range(0, width):
            colored_pixels[i][j][2] = 0
            colored_pixels[i][j][1] = 0
            colored_pixels[i][j][0] = 0
            # Caso de pixel vermelho (linha ímpar e coluna ímpar):
            if(i%2 == 1 and j%2 == 1):
                colored_pixels[i][j][2] = pixels[i][j][2]
                for (m, n) in greenComponent:
                    colored_pixels[i][j][1] = colored_pixels[i][j][1] + (1/4) * getColor(pixels, i + m, j + n)[1]
                for (m, n) in blueComponentAtRed:
                    colored_pixels[i][j][0] = colored_pixels[i][j][0] + (1/4) * getColor(pixels, i + m, j + n)[0]
            # Caso de pixel azul (linha par e coluna par):
            if(i%2 == 0 and j%2 == 0):
                colored_pixels[i][j][0] = pixels[i][j][0]
                for (m, n) in greenComponent:
                    colored_pixels[i][j][1] = colored_pixels[i][j][1] + (1/4) * getColor(pixels, i + m, j + n)[1]
                for (m, n) in redComponentAtBlue:
                    colored_pixels[i][j][2] = colored_pixels[i][j][2] + (1/4) * getColor(pixels, i + m, j + n)[2]
            # Caso de pixel verde (linha mod 2 != coluna mod 2):
            if(i%2 != j%2):
                colored_pixels[i][j][1] = pixels[i][j][1]
                for (m, n) in redComponentAtGreen:
                    colored_pixels[i][j][2] = colored_pixels[i][j][2] + (1/2) * getColor(pixels, i + m, j + n)[2]
                for (m, n) in blueComponentAtGreen:
                    colored_pixels[i][j][0] = colored_pixels[i][j][0] + (1/2) * getColor(pixels, i + m, j + n)[0]
    return colored_pixels

def showImage(pixels):
    cv.imshow("image", pixels)
    print("Aperte 'Esc' para fechar a imagem (não clique no 'X')")
    while True:
        k = cv.waitKey(0)
        if k == 27:
            break
    cv.destroyAllWindows()


if __name__ == "__main__":
    img = cv.imread("/home/bruno/PIM/Imagens para testes/Lighthouse_bayerBG8.png")
    pixels = np.asarray(img)

    height = len(pixels)
    width = len(pixels[0])

    # print(pixels[0][0])

    # Anotação: antes de usar o deepcopy estava ocorrendo problema pois se estava fazendo a media em cima...
    # ... das médias anteriores que zeravam o valor da cor de mosaico de cada pixel antes do cálculo da média...
    # ... sobre o mesmo, dado que a declaração 'colored_pixels = pixels' faz colored_pixels um ponteiro para pixels.

    # colored_pixels = copy.deepcopy(pixels)
    # colored_pixels = np.zeros((height, width, 3), dtype=np.uint8)
    # Obs.: o tipo de array usado em imagem lida pelo opencv tem os valores como np.uint8 (int de 0 - 255).

    colored_pixels = BayerFilter(pixels)
    showImage(pixels)
    showImage(colored_pixels)

    cv.imwrite("Q2.png", colored_pixels)