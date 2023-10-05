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

def getacumulatedfrequency(frequencyArray):
	acumulatedFrequencyArray = []
	count = 0
	for f in frequencyArray:
		count += f
		acumulatedFrequencyArray.append(count)
	return acumulatedFrequencyArray

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
	
def equalizeImage(pixels):
	height = len(pixels)
	width = len(pixels[0])
	frequenceArray = getfrequency(pixels)
	acumulatedFrequencyArray = getacumulatedfrequency(frequenceArray)
	equalized_pixels = np.zeros((height, width), dtype=np.uint8)
	L = 256
	for i in range(0, height):
		for j in range(0, width):
			equalized_pixels[i][j] = (L-1)/(height * width) * acumulatedFrequencyArray[pixels[i][j][1]]
	return equalized_pixels
	
def getSpecification():
	file = open("QD.txt", "r")
	G_array = []
	P_z_sum = 0    
	L = 256
	for q in range(0, 256):
		P_zi = float(file.readline())
		P_z_sum += P_zi
		G_zq = int((L-1)*P_z_sum) 
		G_array.append(G_zq)
	return G_array

def writeSpecification():
	file = open("QD.txt", "w")
	def probabilityFunc(i):
		return 0
	for i in range(0, 256):
		file.write(str(probabilityFunc(i)))
		if(i != 255): 
			file.write("\n")


def G_inverse(s, G_array):
	q = 0
	s = int(s)
	for i in range(0, 256):
		if(abs(G_array[i] - s) <= abs(G_array[q] - s)):
			q = i
	return q

def equalizeImageBySpecification(pixels, G_array):
	height = len(pixels)
	width = len(pixels[0])
	frequenceArray = getfrequency(pixels)
	acumulatedFrequencyArray = getacumulatedfrequency(frequenceArray)
	equalized_pixels = np.zeros((height, width), dtype=np.uint8)
	L = 256
	for i in range(0, height):
		for j in range(0, width):
			s = (L-1)/(height * width) * acumulatedFrequencyArray[pixels[i][j][1]]
			z = G_inverse(s, G_array)
			equalized_pixels[i][j] = z
	return equalized_pixels

if __name__ == "__main__":
	img = cv.imread("taxaPerCapitaRouboCarros.png")
	pixels = np.asarray(img)
	
	equalized_pixels = equalizeImage(pixels)
	showImage(equalized_pixels)

	G_array = getSpecification()
	equalized_pixels = equalizeImageBySpecification(pixels, G_array)
	showImage(equalized_pixels)

	# writeSpecification()