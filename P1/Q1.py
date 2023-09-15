# Alunos: Bruno R. dos Santos e Luigi
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys

# img = cv.imread("/home/bruno/PIM/Imagens para testes/red.png")
img = cv.imread("/home/bruno/PIM/Imagens para testes/green.png")
# img = cv.imread("/home/bruno/PIM/Imagens para testes/blue.png")
# img = cv.imread("/home/bruno/PIM/Imagens para testes/white.png")
# img = cv.imread("/home/bruno/PIM/Imagens para testes/black.png")

pixels = np.asarray(img)

# print(pixels[0][0])

red = {'R' : 255, 'G' : 0, 'B' : 0, "name" : "red"}
green = {'R' : 0, 'G' : 255, 'B' : 0, "name" : "green"}
blue = {'R' : 24, 'G' : 252, 'B' : 255, "name" : "blue"}
white = {'R' : 255, 'G' : 255, 'B' : 255, "name" : "white"}
black = {'R' : 0, 'G' : 0, 'B' : 0, "name" : "black"}

amostras = [red, green, blue, white, black]

average = {'R' : 0, 'G' : 0, 'B' : 0, "name" : "average"}

height = len(pixels)
width = len(pixels[0])

total = height * width

def diff_color(color1 : dict, color2 : dict) -> float:
    dR = abs(color1['R'] - color2['R'])
    dG = abs(color1['G'] - color2['G'])
    dB = abs(color1['B'] - color2['B'])
    return ((dR + dG + dB)/3)

if __name__ == "__main__":

    # Obs.: a imagem está em BGR
    for line in pixels:
        for pixel in line:
            average['R'] = average['R'] + pixel[2] 
            average['G'] = average['G'] + pixel[1] 
            average['B'] = average['B'] + pixel[0] 

    average['R'] = average['R']/total
    average['G'] = average['G']/total
    average['B'] = average['B']/total

    color = amostras[0]
    for item in amostras[1:]:
        if(diff_color(color, average) > diff_color(item, average)):
            color = item

    print(color["name"])