# Alunos: Bruno R. dos Santos e Pedro Vargas T.
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *
from Q2 import *

def magnitude(pixels_x_derivative : np.ndarray, pixels_y_derivative : np.ndarray) -> np.ndarray:
    pixels_magnitude = np.zeros_like(pixels_x_derivative, dtype=np.float64)
    for y in range(0, len(pixels_magnitude)):                                         
        for x in range(0, len(pixels_magnitude[0])):                                  
            pixels_magnitude[y][x] = np.sqrt(pixels_y_derivative[y][x] ** 2 + pixels_x_derivative[y][x] ** 2)
    return pixels_magnitude


if __name__ == "__main__":
    np.set_printoptions(suppress = True)
    np.set_printoptions(linewidth=np.inf)

    image_name = "Lua1_gray"
    image_path = "Imagens/" + image_name
    image_ext = "jpg"   

    gaussianBlurCreateAndSave(image_path, image_ext, 5, 5, 1, True)
    image_name = image_name + "-GaussianFilter" 
    image_path = "Imagens/" + image_name
    image_ext = "png"   

    pixels_x_derivative = xAxisDerivative(image_path, image_ext, sobel_x)
    pixels_y_derivative = yAxisDerivative(image_path, image_ext, sobel_y)
    pixels_magnitude = magnitude(pixels_x_derivative, pixels_y_derivative)

    saveImage(image_path + "-Magnitude" + '.' + image_ext, normalizeNDArray(pixels_magnitude))
