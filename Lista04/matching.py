import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('messi.jpg', cv.IMREAD_GRAYSCALE)
template = cv.imread('ball.png', cv.IMREAD_GRAYSCALE)
w, h = template.shape
# Todos os 6 métodos para comparação em uma lista:
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

for meth in methods:
    img_loop = img.copy()
    # Obtém o valor da variável global com nome do método:
    method = eval(meth)
    # Aplica o template matching:
    res = cv.matchTemplate(img_loop,template,method)
    # Obtém o mínimo e máximo valor de matching (não usados) e as localizações onde...
    # ... cada um destes ocorre respectivamente (utilizadas para desenho do retângulo):
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    print(str(min_val) + ", " + str(max_val))

    # Se o método é TM_SQDIFF ou TM_SQDIFF_NORMED então o menor valor indicará matching:
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        # Caso contrário o valor máximo indicará matching:
        top_left = max_loc

    # Para desenhar o retângulo devemos obter a localização de seu canto inferior direito:
    bottom_right = (top_left[0] + w, top_left[1] + h)
    # OBS.: note que as localização de min e max são dadas pelos canto superior esquerdo...
    # ... em que se inicia uma janela com tamanho do template (uma janela deslizante),...
    # ... por isso não são o centro da onde temos que desenhar o retângulo.

    # Desenhar o retângulo passando imagem, canto superior esquerdo e canto inferior direito,...
    # ... cor e grossura do retângulo: 
    cv.rectangle(img_loop,top_left, bottom_right, 255, 5)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img_loop,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()