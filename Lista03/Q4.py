# Alunos: Bruno R. dos Santos e Pedro Vargas T.
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *

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


def getColorAt(pixels : np.ndarray, x : int, y : int) -> np.float64:
    if(y < 0 or y >= len(pixels) or x < 0 or x >= len(pixels[0])):
        return 0
    return np.float64(pixels[y][x])

def convertToRad(angle : np.float64) -> np.float64:
    # xr/pi = x/180 -> xr = pi * x/180 
    rad_angle = np.pi * angle / 180
    return rad_angle

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

def applyConvolutionAtPixel(old_pixels : np.ndarray, kernel : np.ndarray, x : int, y : int) -> np.int64:
    h, w = kernel.shape
    value = 0
    # Aqui havia o seguinte erro: estava-se sempre pegando a cor do mesmo pixel no uso da função getColorAt() pois...
    # ... não havia nenhuma variável do for sendo usada.
    value = sum(kernel[i][j] * np.float64(getColorAt(old_pixels, x + j - floor(w/2.0), 
                                                    y + i - floor(h/2.0))) for i in range (0, h) for j in range(0, w))
    # if(value >= 256 or value < 0):
    #      print("Overflow")
    return value

def convolution(old_pixels : np.ndarray, kernel : np.ndarray) -> np.ndarray:
    # Obs.: note que dtype deve ser uint8, caso contrário ocorre overflow com números maiores de 7 bits
    new_pixels = np.zeros_like(old_pixels, dtype=np.uint8)
    for y in range(0, len(old_pixels)):
        for x in range(0, len(old_pixels[0])):
                new_pixels[y][x] = np.uint8(applyConvolutionAtPixel(old_pixels, kernel, x, y))
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
    if(flag):
        print(kernel)
        print(kernel.sum())
        # print(sum(pixel for line in kernel for pixel in line))
    pixels = np.asarray(img)
    filter_pixels = convolution(pixels, kernel)
    if(flag):
        saveImage(image_path + "-GaussianFilter.png", filter_pixels)
    return filter_pixels

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

def magnitude(pixels_x_derivative : np.ndarray, pixels_y_derivative : np.ndarray) -> np.ndarray:
    pixels_magnitude = np.zeros_like(pixels_x_derivative, dtype=np.int64)
    for y in range(0, len(pixels_magnitude)):                                         
        for x in range(0, len(pixels_magnitude[0])):                                  
            pixels_magnitude[y][x] = sqrt(pixels_x_derivative[y][x] ** 2 + pixels_y_derivative[y][x] ** 2)
    return pixels_magnitude

def direction(pixels_x_derivative : np.ndarray, pixels_y_derivative : np.ndarray) -> np.ndarray:
    pixels_direction = np.zeros_like(pixels_x_derivative, dtype=np.float64)
    epsilon = 0.0000000000001
    for y in range(0, len(pixels_direction)):                                         
        for x in range(0, len(pixels_direction[0])):        
            pixels_direction[y][x] = np.arctan( pixels_y_derivative[y][x]/(pixels_y_derivative[y][x] + epsilon) )
            # Obs.: a função arctan retorna valores entre pi/2 e -pi/2.   
    return pixels_direction

def edgeDectector(pixels_magnitude : np.ndarray, pixels_direction : np.ndarray) -> np.ndarray:
    pixels_borders = np.zeros_like(pixels_direction, dtype=np.uint8)
    for y in range(0, len(pixels_borders)):                                         
        for x in range(0, len(pixels_borders[0])):          
            # Obs.: a função arctan retorna valores entre pi/2 e -pi/2.   
            if(convertToRad(-22.5) <= pixels_direction[y][x] <= convertToRad(22.5)):
                if(getColorAt(pixels_magnitude, x-1, y) < getColorAt(pixels_magnitude, x, y)
                   and getColorAt(pixels_magnitude, x+1, y) < getColorAt(pixels_magnitude, x, y)):
                    pixels_borders[y][x] = 255
            elif(convertToRad(22.5) < pixels_direction[y][x] <= convertToRad(67.5)):
                if(getColorAt(pixels_magnitude, x-1, y-1) < getColorAt(pixels_magnitude, x, y)
                   and getColorAt(pixels_magnitude, x+1, y+1) < getColorAt(pixels_magnitude, x, y)):
                    pixels_borders[y][x] = 255
            elif(convertToRad(67.5) < pixels_direction[y][x]):
                if(getColorAt(pixels_magnitude, x, y-1) < getColorAt(pixels_magnitude, x, y)
                   and getColorAt(pixels_magnitude, x, y+1) < getColorAt(pixels_magnitude, x, y)):
                    pixels_borders[y][x] = 255
            elif(convertToRad(-67.5) <= pixels_direction[y][x] < convertToRad(-22,5)):
                if(getColorAt(pixels_magnitude, x+1, y-1) < getColorAt(pixels_magnitude, x, y)
                   and getColorAt(pixels_magnitude, x-1, y+1) < getColorAt(pixels_magnitude, x, y)):
                    pixels_borders[y][x] = 255
            elif(pixels_direction[y][x] < convertToRad(-67,5)):
                if(getColorAt(pixels_magnitude, x, y-1) < getColorAt(pixels_magnitude, x, y)
                   and getColorAt(pixels_magnitude, x, y+1) < getColorAt(pixels_magnitude, x, y)):
                    pixels_borders[y][x] = 255
            else:
                pixels_borders[y][x] = 0
    return pixels_borders

if __name__ == "__main__":
    np.set_printoptions(suppress = True)
    np.set_printoptions(linewidth=np.inf)

    # image_path = "Imagens/DIP-XE-GaussianFilter"
    image_path = "Imagens/DIP-XE"

    # image_path = "Imagens/Lua1_gray"
    # image_path = "Imagens/city-GaussianFilter"
    # image_path = "Imagens/img02"
    # image_ext = "png"
    image_ext = "jpg"
    
    gaussianBlur(image_path, image_ext, 3, 3, 3, True)

    image_path = image_path + "-GaussianFilter"
    image_ext = "png"
    
    pixels_x_derivative = xAxisDerivative(image_path, image_ext, sobel_x)
    pixels_y_derivative = yAxisDerivative(image_path, image_ext, sobel_y)
    pixels_magnitude = magnitude(pixels_x_derivative, pixels_y_derivative)
    pixels_direction = direction(pixels_x_derivative, pixels_y_derivative)
    pixels_border = edgeDectector(pixels_magnitude, pixels_direction)
    
    showImage(pixels_border)
    plt.imshow(pixels_border)
    # plt.show()
