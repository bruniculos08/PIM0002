# Alunos: Bruno R. dos Santos e Pedro Vargas T.
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *
from Q5 import *

def gradientDirectionHistogram(pixels_magnitude : np.ndarray, pixels_direction : np.ndarray, interval_size : int) -> np.ndarray:
    histogram = np.zeros(floor(360/interval_size + 1), dtype=float)
    for y in range(0, len(pixels_magnitude)):
        for x in range(0, len(pixels_magnitude[0])):
            # Antes da alteração no código os ângulos eram apenas em valores de -pi/2 até pi/2 (usando a função ...
            # ... np.arctan) mas agora são de -pi até pi (usando a função np.arctan2).
            angle = degrees(pixels_direction[y][x])
            if(pixels_direction[y][x] < 0):
                angle = 360 + degrees(pixels_direction[y][x]) 
            index_aprox = int(floor(angle/interval_size))
            if(index_aprox < angle/interval_size):
                histogram[index_aprox] += pixels_magnitude[y][x]/2.0
                histogram[index_aprox+1] += pixels_magnitude[y][x]/2.0
            else:
                histogram[index_aprox] += pixels_magnitude[y][x]
    return histogram

def showGradientDirectionHistogram(histogram):
    X = np.zeros(len(histogram))
    interval_size = 360 / float(len(histogram)-1)
    for i in range(0, len(histogram)):
       X[i] = i * interval_size
    plt.bar(X, histogram, color = 'maroon', width=1)
    plt.xlabel("Ângulo")
    plt.ylabel("Magnitude")
    plt.title("Histograma")
    plt.show()

if __name__ == "__main__":
    np.set_printoptions(suppress = True)
    np.set_printoptions(linewidth=np.inf)

    image_name = "chessboard_inv"
    image_path = "Imagens/" + image_name
    image_ext = "png"    

    gaussianBlurCreateAndSave(image_path, image_ext, 3, 3, 1, True)
    image_name = image_name + "-GaussianFilter"
    image_path = "Imagens/" + image_name
    image_ext = "png"

    pixels_x_derivative = xAxisDerivative(image_path, image_ext, scharr_x)
    pixels_y_derivative = yAxisDerivative(image_path, image_ext, scharr_y)
    pixels_magnitude = magnitude(pixels_x_derivative, pixels_y_derivative)
    pixels_direction = direction(pixels_x_derivative, pixels_y_derivative)
    pixels_border = edgeDectector(pixels_magnitude, pixels_direction, 1, 0)

    showImage(pixels_border)
    saveImage(image_path + "-Border" + '.' + image_ext, pixels_border)

    histogram = gradientDirectionHistogram(pixels_magnitude, pixels_direction, 1)
    showGradientDirectionHistogram(histogram)
    