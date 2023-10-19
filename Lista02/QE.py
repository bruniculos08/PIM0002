# coding=utf-8
# Alunos: Bruno R. dos Santos e Vinícios Bidin
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *
import skimage

def getfrequency(pixels, channel, imageType):
	frequencyArray = np.zeros((256))
	for line in pixels:
		for pixel in line:
			if(imageType == "RGB"):
				frequencyArray[pixel[channel]] += 1
			else:
				frequencyArray[int(pixel[channel] * 255)] += 1

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

def showImage(pixels, imageType):
	cv.imshow("image", pixels)
	print("Aperte 'Esc' para fechar a imagem (não clique no 'X')")
	while True:
		k = cv.waitKey(0)
		if k == 27:
			break
	cv.destroyAllWindows()

def saveImage(name, pixels):
	cv.imwrite(name, pixels)
	
def equalizeImage(pixels, imageType):
	height = len(pixels)
	width = len(pixels[0])

	if(imageType == "RGB"):
		channels = [0, 1, 2]
		equalized_pixels = np.zeros((height, width, 3), dtype=np.uint8)
	else:
		channels = [0]
		equalized_pixels = np.zeros((height, width, 3), dtype=np.float64)

	for channel in channels:
		frequenceArray = getfrequency(pixels, channel, imageType)
		acumulatedFrequencyArray = getacumulatedfrequency(frequenceArray)
		L = 256
		for i in range(0, height):
			for j in range(0, width):
				if(imageType == "RGB"):
					equalized_pixels[i][j][channel] = (L-1)/(height * width) * acumulatedFrequencyArray[pixels[i][j][channel]]
				else:
					equalized_pixels[i][j][channel] = (L-1)/(height * width) * acumulatedFrequencyArray[int(pixels[i][j][channel] * 255)]/255
					equalized_pixels[i][j][1] = pixels[i][j][1] 
					equalized_pixels[i][j][2] = pixels[i][j][2] 
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
		return (1.0/255.0)
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

def equalizeImageBySpecification(pixels, G_array, imageType):
	height = len(pixels)
	width = len(pixels[0])

	if(imageType == "RGB"):
		channels = [0, 1, 2]
		equalized_pixels = np.zeros((height, width, 3), dtype=np.uint8)
	else:
		channels = [0]
		equalized_pixels = np.zeros((height, width, 3), dtype=np.float64)

	for channel in channels:
		frequenceArray = getfrequency(pixels, channel, imageType)
		acumulatedFrequencyArray = getacumulatedfrequency(frequenceArray)
		L = 256
		for i in range(0, height):
			for j in range(0, width):
				if(imageType == "RGB"):
					s = (L-1)/(height * width) * acumulatedFrequencyArray[pixels[i][j][channel]]
					z = G_inverse(s, G_array)
					equalized_pixels[i][j][channel] = z
				else:
					s = (L-1)/(height * width) * acumulatedFrequencyArray[int(pixels[i][j][channel] * 255)]
					z = G_inverse(s, G_array)
					equalized_pixels[i][j][channel] = z/255
					equalized_pixels[i][j][1] = pixels[i][j][1]
					equalized_pixels[i][j][2] = pixels[i][j][2]
	return equalized_pixels

def integerConvertYQI(pixels):
	height = len(pixels)
	width = len(pixels[0])
	converted_pixels = np.zeros((height, width, 3), dtype=np.uint8)
	for i in range(0, height):
		for j in range(0, width):
			converted_pixels[i][j][0] = int(pixels[i][j][0] * 255)
			converted_pixels[i][j][1] = int(pixels[i][j][1] * 255)
			converted_pixels[i][j][2] = int(pixels[i][j][2] * 255)
	return converted_pixels

if __name__ == "__main__":
	img = cv.imread("predios.jpeg")
	pixels_RGB = np.asarray(img)
	pixels_YIQ = skimage.color.rgb2yiq(img)

	equalized_pixels_YIQ = skimage.color.yiq2rgb(equalizeImage(pixels_YIQ, "YIQ"))
	equalized_pixels_RGB = equalizeImage(pixels_RGB, "RGB")
	showImage(equalized_pixels_YIQ, "YIQ")
	showImage(equalized_pixels_RGB, "RGB")

	# G_array = getSpecification()
	# equalized_pixels_YIQ = skimage.color.yiq2rgb(equalizeImageBySpecification(pixels_YIQ, G_array, "YIQ"))
	# equalized_pixels_RGB = equalizeImageBySpecification(pixels_RGB, G_array, "RGB")
	# showImage(equalized_pixels_YIQ, "YIQ")
	# showImage(equalized_pixels_RGB, "RGB")

	img = cv.imread("outono_LC.png")
	pixels_RGB = np.asarray(img)
	pixels_YIQ = skimage.color.rgb2yiq(img)

	equalized_pixels_YIQ = skimage.color.yiq2rgb(equalizeImage(pixels_YIQ, "YIQ"))
	equalized_pixels_RGB = equalizeImage(pixels_RGB, "RGB")
	showImage(equalized_pixels_YIQ, "YIQ")
	showImage(equalized_pixels_RGB, "RGB")

	# G_array = getSpecification()
	# equalized_pixels_YIQ = skimage.color.yiq2rgb(equalizeImageBySpecification(pixels_YIQ, G_array, "YIQ"))
	# equalized_pixels_RGB = equalizeImageBySpecification(pixels_RGB, G_array, "RGB")
	# showImage(equalized_pixels_YIQ, "YIQ")
	# showImage(equalized_pixels_RGB, "RGB")