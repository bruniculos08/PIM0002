# Alunos: Bruno R. dos Santos e Pedro Vargas T.
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *

def getColorAt(pixels : np.ndarray, x : int, y : int) -> np.float64:
    if(y < 0 or y >= len(pixels) or x < 0 or x >= len(pixels[0])):
        return 0
    return np.float64(pixels[y][x])

def normalizeNDArray(pixels : np.ndarray) -> np.ndarray:
    max_value = pixels.max()
    new_pixels = np.zeros_like(pixels, dtype=np.uint8)
    h, w = pixels.shape
    for i in range(0, h):
        for j in range(0, w):
            new_pixels[i][j] = np.uint8((pixels[i][j]/max_value) * 255)
    return new_pixels

def roundDependentSignal(k):
     if(k > 0):
          return floor(k)
     return ceil(k)

def applyConvolutionAtPixel(old_pixels : np.ndarray, kernel : np.ndarray, x : int, y : int) -> np.int8:
    h, w = kernel.shape
    value = 0

    # gauss = [[1/16, 1/8, 1/16],
    #          [1/8, 1/4, 1/8],
    #          [1/16, 1/8, 1/16]]
    

    # for i in range(-1, 1):
    #      for j in range(-1, 1):
    #             value = value + (gauss[i][j] * old_pixels[y+i][x+j])

    # Aqui havia o seguinte erro: estava-se sempre pegando a cor do mesmo pixel no uso da função getColorAt() pois...
    # ... não havia nenhuma variável do for sendo usada.
    value = sum(kernel[i][j] * np.float64(getColorAt(old_pixels, x + j - floor(w/2.0), 
                                                    y + i - floor(h/2.0))) for i in range (0, h) for j in range(0, w))

    if(value >= 255 or value <= 0):
         print("Overflow")

    return np.int8(value)

def convolution(old_pixels : np.ndarray, kernel : np.ndarray) -> np.ndarray:
    new_pixels = np.zeros_like(old_pixels, dtype=np.uint8)
    for y in range(0, len(old_pixels)):
        for x in range(0, len(old_pixels[0])):
            new_pixels[y][x] = applyConvolutionAtPixel(old_pixels, kernel, x, y)
    return new_pixels

def discreteGaussianFunction(x : np.float64, y : np.float64, standard_deviation : np.float64, mean_x : np.float64, mean_y : np.float64) -> np.float64:
    x = (x - mean_x)
    y = (y - mean_y)
    return (1/(2 * np.pi * (standard_deviation ** 2.0))) * np.exp(-(x**2.0 + y**2.0)/(2.0 * (standard_deviation ** 2.0)))

def calcGaussianKernel(kernel_height : int, kernel_width : int, standard_deviation : np.float64) -> np.ndarray:
    gaussian_kernel = np.zeros((kernel_height, kernel_width), dtype=np.float64)
    for y in range(0, len(gaussian_kernel)):
        for x in range(0, len(gaussian_kernel[0])):
            gaussian_kernel[y][x] = discreteGaussianFunction(np.float64(x), np.float64(y), 
                                                            standard_deviation, np.float64(floor(kernel_width/2)), np.float64(floor(kernel_height/2)))
    normalize_value = np.float64(sum(pixel for line in gaussian_kernel for pixel in line))
    gaussian_kernel = gaussian_kernel/normalize_value
    return gaussian_kernel

def showImage(pixels):
	cv.imshow("image", pixels)
	print("Aperte 'Esc' para fechar a imagem (não clique no 'X')")
	while True:
		k = cv.waitKey(0)
		if k == 27:
			break
	cv.destroyAllWindows()
     
def saveImage(name, pixels):
	cv.imwrite(name, pixels)
     
def gaussianBlur(image_path : str, image_ext : str, kernel_height : int, kernel_width : int, standard_deviation : int, flag : bool = False) -> np.ndarray:
    img = cv.imread(image_path + '.' + image_ext, cv.IMREAD_GRAYSCALE)
    kernel = calcGaussianKernel(kernel_height, kernel_width, standard_deviation)
    # print(kernel)
    # print(sum(pixel for line in kernel for pixel in line))
    pixels = np.asarray(img)
    filter_pixels = convolution(pixels, kernel)
    if(flag == True):
        saveImage(image_path + "-GaussianFilter.png", filter_pixels)
    return filter_pixels

if __name__ == "__main__":
    np.set_printoptions(suppress = True)
    np.set_printoptions(linewidth=np.inf)

    image_path = "Imagens/city"
    image_ext = "png"
    filter_pixels = gaussianBlur(image_path, image_ext, 5, 5, 3, True)