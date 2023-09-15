# Alunos: Bruno R. dos Santos e Luigi
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
import copy

def showImage(pixels):
    cv.imshow("image", pixels)
    print("Aperte 'Esc' para fechar a imagem (não clique no 'X')")
    while True:
        k = cv.waitKey(0)
        if k == 27:
            break
    cv.destroyAllWindows()

def GreyFilter(pixels):
    height = len(pixels)
    width = len(pixels[0])
    colored_pixels = np.zeros((height, width), dtype=np.uint8)
    # Obs.: a imagem está em BGR.
    for i in range(0, height):
        for j in range(0, width):
            colored_pixels[i][j] = float(pixels[i][j][2]) * 0.299 + float(pixels[i][j][1]) * 0.587 + float(pixels[i][j][0]) * 0.144
            # colored_pixels[i][j] = (float(pixels[i][j][2]) + float(pixels[i][j][1]) + float(pixels[i][j][0]))/3
            # colored_pixels[i][j] = min(pixels[i][j][2], pixels[i][j][1], pixels[i][j][0])/2 + max(pixels[i][j][2], pixels[i][j][1], pixels[i][j][0])/2 

    return colored_pixels

def getFrequence(pixels):
    height = len(pixels)
    width = len(pixels[0])
    frequenceArray = np.zeros((256))

    for line in pixels:
        for pixel in line:
            frequenceArray[pixel] += 1

    return frequenceArray

def showFrequence(frequenceArray):
    X = np.zeros((256))
    for i in range(0, 256):
        X[i] = i
    plt.bar(X, frequenceArray, color ='maroon',
        width = 0.4)
 
    plt.xlabel("Valor")
    plt.ylabel("Frequência")
    plt.title("Histograma")
    plt.show()

def calcLimiar(frequenceArray, percentDiff):
    t = 127
    u1 = u2 = 0
    percentDiff = percentDiff/100
    diff = 1
    while diff > percentDiff:
        u1 = sum(i * frequenceArray[i] for i in range(0, int(t)))/sum(frequenceArray[i] for i in range(0, int(t)))
        u2 = sum(i * frequenceArray[i] for i in range(int(t), 256))/sum(frequenceArray[i] for i in range(int(t), 256))
        diff = abs(t - (u1 + u2)/2)/t 
        t = (u1 + u2)/2
    return t

def LimiarFilter(pixels, t, low, hight):
    height = len(pixels)
    width = len(pixels[0])

    limiar_pixels = np.zeros((height, width), dtype=np.uint8)
    # Obs.: a imagem está em BGR.
    for i in range(0, height):
        for j in range(0, width):
            if(pixels[i][j] < t):
                limiar_pixels[i][j] = low
            else:
                limiar_pixels[i][j] = hight
        
    return limiar_pixels

if __name__ == "__main__":
    img = cv.imread("/home/bruno/PIM/P1/Q2.png")
    pixels = np.asarray(img)

    grey_pixels = GreyFilter(pixels)
    showImage(grey_pixels)

    frequenceArray = getFrequence(grey_pixels)
    showFrequence(frequenceArray)
    t = calcLimiar(frequenceArray, 0.1)
    limiar_pixels = LimiarFilter(grey_pixels, t, 0, 255)
    showImage(limiar_pixels)

    cv.imwrite("Q3 - Grey Filter.png", grey_pixels)
    cv.imwrite("Q3 - Limiar Filter.png", limiar_pixels)
