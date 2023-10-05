# coding=utf-8
# Alunos: Bruno R. dos Santos e Vinícios Bidin
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *

# Funções relacionadas a frequência global de intensidades (de pixels) na imagem:

def getFrequency(pixels):
	frequencyArray = np.zeros(256)
	for line in pixels:
		for pixel in line:
			frequencyArray[pixel] += 1
	return frequencyArray

def getAcumulatedFrequency(frequencyArray):
	acumulatedFrequencyArray = []
	count = 0
	for f in frequencyArray:
		count += f
		acumulatedFrequencyArray.append(count)
	return acumulatedFrequencyArray

def showFrequency(frequencyArray):
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

def saveFrequency(name, frequencyArray):
	X = np.zeros((256))
	for i in range(0, 256):
		X[i] = i
	plt.bar(X, frequencyArray, color ='maroon',width = 0.4)
	plt.xlabel("Valor")
	plt.ylabel("Frequência")
	plt.title("Histograma")
	plt.savefig(name)

# Funções para mostrar e salvar imagem:

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
	
# Equalização de imagem padrão:

def equalizeImage(pixels):
	height = len(pixels)
	width = len(pixels[0])
	frequencyArray = getFrequency(pixels)
	acumulatedFrequencyArray = getAcumulatedFrequency(frequencyArray)
	equalized_pixels = np.zeros((height, width), dtype=np.uint8)
	L = 256
	for i in range(0, height):
		for j in range(0, width):
			equalized_pixels[i][j] = (L-1)/(height * width) * acumulatedFrequencyArray[pixels[i][j]]
	return equalized_pixels
	
def equalizerImageLocally(pixels, equalized_pixels, i, j, height, width):
	frequencyArray = np.zeros(256)
	for y in range(i - ceil(height/2), i + floor(height/2)):
		for x in range(j - ceil(width/2), j + floor(width/2)):
			if(0 <= y < len(pixels) and 0 <= x < len(pixels[0])):
				frequencyArray[pixels[y][x]] += 1
			else:
				frequencyArray[0] += 1

	acumulatedFrequencyArray = getAcumulatedFrequency(frequencyArray)

	L = 256
	equalized_pixels[i][j] = (L-1)/(height * width) * acumulatedFrequencyArray[pixels[i][j]]

def equalizerImageLocallyForAll(pixels, equalized_pixels, height, width):
	for i in range(0, len(pixels)):
		for j in range(0, len(pixels[0])):
			equalizerImageLocally(pixels, equalized_pixels, i, j, height, width)

# Equalização de imagem por método que utiliza média e desvio padrão:

def calcAverage(frequencyArray, pixels):
	return sum(i * frequencyArray[i]/(len(pixels) * len(pixels[0])) for i in range(0, 256))

def calcStandardDeviation(frequencyArray, pixels):
	avg = calcAverage(frequencyArray, pixels)
	return sum( ((i - avg)**2) * (frequencyArray[i] / (len(pixels) * len(pixels[0]))) for i in range(0, 256))

def calcLocalFrequency(pixels, i, j, height, width):
	localFrequencyArray = np.zeros(256)
	for y in range(i - ceil(height/2), i + floor(height/2)):
		for x in range(j - ceil(width/2), j + floor(width/2)):
			if(0 <= y < len(pixels) and 0 <= x < len(pixels[0])):
				localFrequencyArray[pixels[y][x]] += 1
			else:
				localFrequencyArray[0] += 1
	return localFrequencyArray

def calcLocalMean(height, width, localFrequencyArray):
	L = 256
	return sum(i * localFrequencyArray[i]/(height * width) for i in range(0, L))

def calcLocalStandardDeviation(local_mean, height, width, localFrequencyArray):
	L = 256
	return sum(	((i-local_mean) ** 2) * (localFrequencyArray[i]/(height * width)) for i in range(0, L))

def gEnhancementApply(pixels, enhanced_pixels, window_height, window_width):
	global_frequency_array = getFrequency(pixels)
	global_mean = calcAverage(global_frequency_array, pixels)
	global_deviation = calcStandardDeviation(global_frequency_array, pixels)

	for i in range(0, len(pixels)):
		for j in range(0, len(pixels[0])):
			gEnhancement(pixels, enhanced_pixels, i, j, window_height, window_width, global_mean, global_deviation)
	
	return enhanced_pixels

def gEnhancement(pixels, enhanced_pixels, i, j, window_height, window_width, global_mean, global_deviation):
	k0 = 0.4
	k1 = 0.02
	k2 = 0.4
	E = 4

	local_frequency_array = calcLocalFrequency(pixels, i, j, window_height, window_width)
	local_mean = calcLocalMean(window_height, window_width, local_frequency_array)
	local_deviation = calcLocalStandardDeviation(local_mean, window_height, window_width, local_frequency_array)

	if(local_mean <= k0 * global_mean and k1 * sqrt(global_deviation) <= sqrt(local_deviation) <= k2 * sqrt(global_deviation)):
		enhanced_pixels[i][j] = (E * pixels[i][j]) % 256
	else:
		enhanced_pixels[i][j] = pixels[i][j]

if __name__ == "__main__":
	img = cv.imread("cabeloGonzalez.png", cv.IMREAD_GRAYSCALE)
	pixels = np.asarray(img)
	equalized_pixels = np.zeros((len(pixels), len(pixels[0])), dtype=np.uint8)

	equalized_pixels = equalizeImage(pixels)
	showImage(equalized_pixels)

	# equalizerImageLocallyForAll(pixels, equalized_pixels, 3, 3)
	# showImage(equalized_pixels)

	equalized_pixels = gEnhancementApply(pixels, equalized_pixels, 3, 3)
	showImage(equalized_pixels)
	# showImage(pixels)

	# writeSpecification()