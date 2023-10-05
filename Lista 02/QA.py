#
# Alunos: Bruno R. dos Santos e Vinícios Bidin
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *

def getfrequency(pixels):
	frequencyArray = np.zeros((256))
	for line in pixels:
		for pixel in line:
			frequencyArray[pixel] += 1
	return frequencyArray

def showfrequency(frequencyArray):
	X = np.zeros((256))
	for i in range(0, 256):
		X[i] = i
	plt.bar(X, frequencyArray, color ='maroon', width = 0.4)
	plt.xlabel("Valor")
	plt.ylabel("Frequência")
	axis = plt.gca()
	axis.set_ylim([max(f for f in frequencyArray), max(f for f in frequencyArray)])
	plt.title("Histograma")
	plt.show()

def savefrequency(name, frequencyArray):
	X = np.zeros((256))
	for i in range(0, 256):
		X[i] = i
	plt.bar(X, frequencyArray, color ='maroon',width = 0.4)
	plt.xlabel("Valor")
	plt.ylabel("Frequência")
	plt.title("Histograma")
	plt.savefig(name)

# def makeColorDict(frequencyArray : list) -> dict:
# 	color_per_grey_value= {}
# 	actual_color = [50, 50, 0]
# 	count = sum(1 for x in frequence_array if x > 0)
# 	j = 0
# 	for i in range(0, 256):
# 		actual_color[2] = i
# 		j += 1
# 		if(frequence_array[i] > 0):
# 			color_per_grey_value[i] = actual_color

def colorizeImage(pixels, colored_pixels):
	for i in range(0, len(pixels)):
		for j in range(0, len(pixels[0])):
			colored_pixels[i][j] = [255, 255, 255]	
			if(0 < pixels[i][j][2] < 255):
				colored_pixels[i][j][0] = 255 * cos(pixels[i][j][2] + pi/2)
				colored_pixels[i][j][1] = 255 * cos(pixels[i][j][2]/2)
				colored_pixels[i][j][2] = 255 * cos(pixels[i][j][2])

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

if __name__ == "__main__":
	img = cv.imread("taxaPerCapitaRouboCarros.png")
	pixels = np.asarray(img)
	height = len(pixels)
	width = len(pixels[0])

	colored_pixels = np.zeros((height, width, 3), dtype=np.uint8)
	frequence_array = getfrequency(pixels)
	colorizeImage(pixels, colored_pixels)

	showImage(colored_pixels)	