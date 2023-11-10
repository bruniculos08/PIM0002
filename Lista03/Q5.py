# Alunos: Bruno R. dos Santos e Pedro Vargas T.
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *
from Q4 import *

def edgeDectector(pixels_magnitude : np.ndarray, pixels_direction : np.ndarray, weight : np.float64 = 1, threshold : np.float64 = 0) -> np.ndarray:
    pixels_borders = np.zeros_like(pixels_direction, dtype=np.uint8)
    for y in range(0, len(pixels_borders)):                                         
        for x in range(0, len(pixels_borders[0])):          
            # Obs.: a função np.arctan2 retorna valores entre pi e -pi.   
            if(pixels_magnitude[y][x] >= threshold):

                angle = np.degrees(pixels_direction[y][x])
                if(pixels_direction[y][x] < 0):
                    angle = 360.0 + np.degrees(pixels_direction[y][x]) 

                if((np.float64(0.0) <= angle <= np.float64(22.5)) or (np.float64(337.5) <= angle <= np.float64(360.0)) 
                   or (np.float64(157.5) <= angle <= np.float64(202.5))):
                    if(getColorAt(pixels_magnitude, x-1, y) * weight < pixels_magnitude[y][x]
                    and getColorAt(pixels_magnitude, x+1, y) * weight < pixels_magnitude[y][x]):
                        pixels_borders[y][x] = 255
                elif((np.float64(22.5) <= angle <= np.float64(67.5)) or (np.float64(202.5) <= angle <= np.float64(247.5))):
                    if(getColorAt(pixels_magnitude, x-1, y-1) * weight < pixels_magnitude[y][x]
                    and getColorAt(pixels_magnitude, x+1, y+1) * weight < pixels_magnitude[y][x]):
                        pixels_borders[y][x] = 255
                elif((np.float64(67.5) <= angle <= np.float64(112.5)) or (np.float64(247.5) <= angle <= np.float64(292.5))):
                    if(getColorAt(pixels_magnitude, x, y-1) * weight < pixels_magnitude[y][x]
                    and getColorAt(pixels_magnitude, x, y+1) * weight < pixels_magnitude[y][x]):
                        pixels_borders[y][x] = 255
                elif((np.float64(112.5) <= angle <= np.float64(157.5)) or (np.float64(292.5) <= angle <= np.float64(337.5))):
                    if(getColorAt(pixels_magnitude, x+1, y-1) * weight < pixels_magnitude[y][x]
                    and getColorAt(pixels_magnitude, x-1, y+1) * weight < pixels_magnitude[y][x]):
                        pixels_borders[y][x] = 255
                else:
                    pixels_borders[y][x] = 0
            else:
                pixels_borders[y][x] = 0
    return pixels_borders

# def edgeDectector(pixels_magnitude : np.ndarray, pixels_direction : np.ndarray, weight : np.float64 = 1, threshold : np.float64 = 0) -> np.ndarray:
#     pixels_borders = np.zeros_like(pixels_direction, dtype=np.uint8)
#     for y in range(0, len(pixels_borders)):                                         
#         for x in range(0, len(pixels_borders[0])):          
#             # Obs.: a função np.arctan retorna valores entre pi/2 e -pi/2.   
#             if(pixels_magnitude[y][x] >= threshold):
#                 if(radians(-22.5) <= pixels_direction[y][x] <= radians(22.5)):
#                     if(getColorAt(pixels_magnitude, x-1, y) * weight < pixels_magnitude[y][x]
#                     and getColorAt(pixels_magnitude, x+1, y) * weight < pixels_magnitude[y][x]):
#                         pixels_borders[y][x] = 255
#                 elif(radians(22.5) < pixels_direction[y][x] <= radians(67.5)):
#                     if(getColorAt(pixels_magnitude, x-1, y-1) * weight < pixels_magnitude[y][x]
#                     and getColorAt(pixels_magnitude, x+1, y+1) * weight < pixels_magnitude[y][x]):
#                         pixels_borders[y][x] = 255
#                 elif(radians(67.5) < pixels_direction[y][x]):
#                     if(getColorAt(pixels_magnitude, x, y-1) * weight < pixels_magnitude[y][x]
#                     and getColorAt(pixels_magnitude, x, y+1) * weight < pixels_magnitude[y][x]):
#                         pixels_borders[y][x] = 255
#                 elif(radians(-67.5) <= pixels_direction[y][x] < radians(-22.5)):
#                     if(getColorAt(pixels_magnitude, x+1, y-1) * weight < pixels_magnitude[y][x]
#                     and getColorAt(pixels_magnitude, x-1, y+1) * weight < pixels_magnitude[y][x]):
#                         pixels_borders[y][x] = 255
#                 elif(pixels_direction[y][x] < radians(-67.5)):
#                     if(getColorAt(pixels_magnitude, x, y-1) * weight < pixels_magnitude[y][x]
#                     and getColorAt(pixels_magnitude, x, y+1) * weight < pixels_magnitude[y][x]):
#                         pixels_borders[y][x] = 255
#                 else:
#                     pixels_borders[y][x] = 0
#             else:
#                 pixels_borders[y][x] = 0
#     return pixels_borders


def averageValue(pixels : np.ndarray) -> np.float64:
    return pixels.sum()/(len(pixels) * len(pixels[0]))

if __name__ == "__main__":
    np.set_printoptions(suppress = True)
    np.set_printoptions(linewidth=np.inf)

    image_name = "Lua1_gray"
    image_path = "Imagens/" + image_name
    image_ext = "jpg"    

    gaussianBlurCreateAndSave(image_path, image_ext, 3, 3, 1, True)
    image_name = image_name + "-GaussianFilter"
    image_path = "Imagens/" + image_name
    image_ext = "png"

    pixels_x_derivative = xAxisDerivative(image_path, image_ext, prewit_x)
    pixels_y_derivative = yAxisDerivative(image_path, image_ext, prewit_y)
    pixels_magnitude = magnitude(pixels_x_derivative, pixels_y_derivative)
    pixels_direction = direction(pixels_x_derivative, pixels_y_derivative)
    pixels_border = edgeDectector(pixels_magnitude, pixels_direction, 1, 0)

    gradient_matrix = "prewit"

    showImage(pixels_border)
    saveImage(image_path + "-Border-" + gradient_matrix + '.' + image_ext, pixels_border)

    # Para comparação com a função implementada na biblioteca OpenCV:
    image = cv.imread(image_path + '.' + image_ext)
    image_library = cv.Canny(image, 0, 0)
    showImage(np.asarray(image_library))