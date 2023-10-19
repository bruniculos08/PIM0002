import numpy as np
from skimage import img_as_ubyte
from skimage.io import imread, imsave
from skimage.color import rgb2yiq, yiq2rgb

def equalizeHistChannel(channel):
    hist, bins = np.histogram(channel, 256, [0, 1])
    cdf = hist.cumsum()
    if cdf[-1] == 0:
        return channel
    cdf_normalized = cdf / cdf[-1]
    equalized = np.interp(channel, bins[:-1], cdf_normalized)
    return equalized

def equalizeImage(image_path):
    image = imread(image_path)

    yiq = rgb2yiq(image)

    y_eq = equalizeHistChannel(yiq[:, :, 0])
    yiq[:, :, 0] = y_eq

    yiq2rgb_eq = yiq2rgb(yiq)
    yiq2rgb_eq = np.clip(yiq2rgb_eq, 0, 1)

    return yiq2rgb_eq

if __name__ == "__main__":
    outono_yiq_equalized = equalizeImage("outono_LC.png")
    predios_yiq_equalized = equalizeImage("predios.jpeg")

    outono_yiq_equalized = img_as_ubyte(outono_yiq_equalized)
    predios_yiq_equalized = img_as_ubyte(predios_yiq_equalized)

    imsave("outono_LC_YIQ_equalized.png", outono_yiq_equalized)
    imsave("predios_YIQ_equalized.png", predios_yiq_equalized)
