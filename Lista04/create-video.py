import cv2 as cv
import os
from glob import glob

def getImgIndex(img_path : str) -> int:
    index = img_path.split("/")[-1].split(".")[0].replace("im", '')
    return int(index)

def showImage(pixels):
    cv.imshow("image", pixels)
    print("Aperte 'Esc' para fechar a imagem (não clique no 'X')")
    while True:
        k = cv.waitKey(0)
        if(k==27 or cv.waitKey(1)):
            break
    cv.destroyAllWindows()

if __name__ == "__main__":
    frames_path = glob("Results/Result-video-teste/TM_SQDIFF_NORMED/im*.png")
    frames_path = sorted(frames_path, key=getImgIndex)

    img_example = cv.imread(frames_path[0], cv.IMREAD_GRAYSCALE)
    w, h = (img_example.shape[1], img_example.shape[0])
    
    # Contruir string do codec do video:
    fourcc = cv.VideoWriter_fourcc('M','J','P','G')
    video_file = cv.VideoWriter("video-teste-template.avi", fourcc, 30.0, (w, h), False)

    for frame_path in frames_path:
        frame = cv.imread(frame_path, cv.IMREAD_GRAYSCALE)
        video_file.write(frame)