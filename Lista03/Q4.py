# Alunos: Bruno R. dos Santos e Pedro Vargas T.
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *
from Q3 import *

def direction(pixels_x_derivative : np.ndarray, pixels_y_derivative : np.ndarray) -> np.ndarray:
    pixels_direction = np.zeros_like(pixels_x_derivative, dtype=np.float64)
    epsilon = 10 ** (-8)
    for y in range(0, len(pixels_direction)):                                         
        for x in range(0, len(pixels_direction[0])):
            pixels_direction[y][x] = np.float64(np.arctan2(pixels_y_derivative[y][x], pixels_x_derivative[y][x]))
            # pixels_direction[y][x] = np.float64(np.arctan(pixels_y_derivative[y][x]/ (pixels_x_derivative[y][x] + epsilon)))
            
            # Obs. 1: a função np.arctan retorna valores entre -pi/2 e pi/2.
            
            # Obs. 2: a função np.arctan2 retorna valores entre -pi e pi e não é necessário o epsilon adicionado...
            # ... ao denominador pois a esta função impede divisões por zero, tendo casos especiais para quando...
            # ... o denominador é zero.   
    return pixels_direction

if __name__ == "__main__":
    np.set_printoptions(suppress = True)
    np.set_printoptions(linewidth=np.inf)

    image_name = "Lua1_gray"
    image_path = "Imagens/" + image_name
    image_ext = "jpg"

    pixels_x_derivative = xAxisDerivative(image_path, image_ext, sobel_x)
    pixels_y_derivative = yAxisDerivative(image_path, image_ext, sobel_y)
    pixels_direction = direction(pixels_x_derivative, pixels_y_derivative)

    saveImage(image_path + "-Direction" + '.' + image_ext, pixels_direction)