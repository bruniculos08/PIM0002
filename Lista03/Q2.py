# Alunos: Bruno R. dos Santos e Pedro Vargas T.
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *
from Q1 import *

prewit_x = np.asarray(
        [[-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]])

prewit_y = np.asarray(
        [[-1, -1, -1],
        [0, 0, 0],
        [1, 1, 1]])

sobel_x = np.asarray([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]])

sobel_y = np.asarray([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]])

scharr_x = np.asarray(
            [[-3, 0, 3],
            [-10, 0, 10],
            [-3, 0, 3]])

scharr_y = np.asarray(
            [[-3, -10, -3],
            [0, 0, 0],
            [3, 10, 3]])
     
def xAxisDerivative(image_path : str, image_ext : str, operator : np.ndarray = prewit_x) -> np.ndarray:
    img = cv.imread(image_path + '.' + image_ext, cv.IMREAD_GRAYSCALE)
    pixels = np.asarray(img)
    pixels_x_derivative = np.zeros_like(pixels, dtype=np.int64)
    for y in range(0, len(pixels)):                                         # linhas
        for x in range(0, len(pixels[0])):                                  # colunas
            pixels_x_derivative[y][x] = applyConvolutionAtPixel(pixels, operator, x, y) 
    return pixels_x_derivative

def yAxisDerivative(image_path : str, image_ext : str, operator : np.ndarray = prewit_y) -> np.ndarray:
    img = cv.imread(image_path + '.' + image_ext, cv.IMREAD_GRAYSCALE)
    pixels = np.asarray(img)
    pixels_y_derivative = np.zeros_like(pixels, dtype=np.int64)
    for y in range(0, len(pixels)):                                         
        for x in range(0, len(pixels[0])):                                  
            pixels_y_derivative[y][x] = applyConvolutionAtPixel(pixels, operator, x, y) 
    return pixels_y_derivative

if __name__ == "__main__":
    np.set_printoptions(suppress = True)
    np.set_printoptions(linewidth=np.inf)

    image_name = "chessboard_inv"
    image_path = "Imagens/" + image_name
    image_ext = "png"    

    gaussianBlurCreateAndSave(image_path, image_ext, 5, 5, 1, True)
    image_name = image_name + "-GaussianFilter"
    image_path = "Imagens/" + image_name
    image_ext = "png"

    pixels_x_derivative = xAxisDerivative(image_path, image_ext, sobel_x)
    pixels_y_derivative = yAxisDerivative(image_path, image_ext, sobel_y)
    saveImage(image_path + "-DerivativeX" + '.' + image_ext, pixels_x_derivative)
    saveImage(image_path + "-DerivativeY" + '.' + image_ext, pixels_y_derivative)