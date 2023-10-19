# Alunos: Bruno R. dos Santos e Vinícios Bidin
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *

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

def GreyFilter(pixels):
	height = len(pixels)
	width = len(pixels[0])
	colored_pixels = np.zeros((height, width), dtype=np.uint8)
	for i in range(0, height):
		for j in range(0, width):
			colored_pixels[i][j] = float(pixels[i][j][2]) * 0.299 + float(pixels[i][j][1]) * 0.587 + float(pixels[i][j][0]) * 0.144
	frequencyArray = np.zeros((256))

	for line in pixels:
		for pixel in line:
			frequencyArray[pixel] += 1

	return frequencyArray

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
	plt.bar(X, frequencyArray, color ='maroon',
		width = 0.4)
 
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
	plt.bar(X, frequencyArray, color ='maroon',
		width = 0.4)
 
	plt.xlabel("Valor")
	plt.ylabel("Frequência")
	plt.title("Histograma")
	plt.savefig(name)

def calcLimiar(frequencyArray, percentDiff):
	t = 127
	u1 = u2 = 0
	percentDiff = percentDiff/100
	diff = 1
	while diff > percentDiff:
		u1 = sum(i * frequencyArray[i] for i in range(0, int(t)))/sum(frequencyArray[i] for i in range(0, int(t)))
		u2 = sum(i * frequencyArray[i] for i in range(int(t), 256))/sum(frequencyArray[i] for i in range(int(t), 256))
		diff = abs(t - (u1 + u2)/2)/t 
		t = (u1 + u2)/2
	return t

def LimiarFilter(pixels, t, low, hight):
	height = len(pixels)
	width = len(pixels[0])

	limiar_pixels = np.zeros((height, width), dtype=np.uint8)
	# Obs.: a imagem está em BGR.
	for i in range(0, height):
		for j in range(0, width):
			if(pixels[i][j] < t):
				limiar_pixels[i][j] = low
			else:
				limiar_pixels[i][j] = hight
		
	return limiar_pixels

def calcAverage(frequencyArray):
	return sum(i * frequencyArray[i] for i in range(0, int(256))) / sum(frequencyArray[i] for i in range(0, 256))

def calcStandardDeviation(frequencyArray):
	avg = calcAverage(frequencyArray)
	return sqrt(sum((frequencyArray[i] - avg)**2 / sum(frequencyArray[i]) for i in range(0, 256)))

def cutImage(pixels, i, j, width, height):
	height_original = len(pixels)
	width_original = len(pixels[0])
	new_pixels = []
	for y in range(i - ceil(height / 2), i + floor(height / 2)):
		line = []
		if (0 <= y < height_original):
			for x in range(j - ceil(width / 2), j + floor(width / 2)):
				if(0 <= x < width_original):
					line.append(pixels[y][x])
			new_pixels.append(line)
	return np.asarray(new_pixels)

# def cutImagefrequency(pixels, i, j, width, height):
# 	height_original = len(pixels)
# 	width_original = len(pixels[0])
# 	frequencyArray = np.zeros((256))
# 	for y in range(i - ceil(height / 2), i + floor(height / 2)):
# 			for x in range(j - ceil(width / 2), j + floor(width / 2)):
# 				if (0 <= y < height_original) and (0 <= x < width_original):
# 					frequencyArray[pixels[y][x]] += 1
# 				else:
# 					frequencyArray[0] += 1
# 	return frequencyArray

def cutImagefrequency(new_pixels, width, height):
	diff_height = height - len(new_pixels)
	diff_width = width - len(new_pixels[0])

	frequencyArray = getfrequency(new_pixels)
	# frequencyArray[0] = diff_width * (diff_height + height) + width * diff_height
	frequencyArray[0] = (diff_width + width) * (diff_height + height) - (width * height)
	return frequencyArray

if __name__ == "__main__":
	img = cv.imread("imagem.png")
	pixels = np.asarray(img)

	# i = int(input("i: "))
	# j = int(input("j: "))
	# width = int(input("width: "))
	# height = int(input("width: "))

	i = 400
	j = 400
	width = 50
	height = 50

	new_pixels = cutImage(pixels, i, j, width, height)
	frequencyArray = cutImagefrequency(new_pixels, width, height)

	savefrequency("frequency.png", frequencyArray)
	saveImage("cut.png", new_pixels)
	
	showfrequency(frequencyArray)
	showImage(new_pixels)
