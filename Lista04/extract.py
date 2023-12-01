import os
import numpy as np
import cv2 as cv
from glob import glob

def createDir(path):
    if os.path.exists(path) == False:
        os.makedirs(path)

def saveFrame(video_path, save_dir):
    name = video_path.split("/")[-1].split(".")[0]
    save_path = os.path.join(save_dir, name)
    
    createDir(save_path)

    index = 0
    video = cv.VideoCapture(video_path)
    while True:
        result, frame = video.read()

        if result == False:
            video.release()
            break

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imwrite(f"{save_path}/im{index}.png", gray_frame)
        index += 1

if __name__ == "__main__":
    video_paths = glob("Videos/*")
    save_dir = "Frames-extracted"

    for path in video_paths:
        saveFrame(path, save_dir)