import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from glob import glob
import os
import csv

def createDir(path):
    if os.path.exists(path) == False:
        os.makedirs(path)

def matchTemplate(meth, img, template, save_path, save_name, option_save_img):
    img_match = img.copy()
    method = eval(meth)
    result = cv.matchTemplate(img_match, template, method)
    w, h = template.shape
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if option_save_img:
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img_match, top_left, bottom_right, 255, 5)
        cv.imwrite(f"{save_path}/{save_name}.png", img_match)

    return min_val, max_val

def buildGraph(csv_file_path : str):
    csv_file = open(csv_file_path, "r")
    method_name, fields, rows, X = [], [], [], []
    method_name = next(csv_file)
    fields = next(csv_file).replace("\n", '').split(",")
    values = [[] for _ in fields]
    values_by_field = dict(zip(fields, values))

    index = 0
    for row in csv_file:
        # rows.append(row)

        row_in_list = row.replace("\n", '').split(",")
        # print(row_in_list)
        
        for column, field in enumerate(fields, 0):
            if(column > 0):
                values_by_field[field].append(float(row_in_list[column]))
            else:
                values_by_field[field].append(row_in_list[column])

        X.append(index)
        index += 1

    for field in fields[1:]:
        plt.plot(X, values_by_field[field], label = field)

    plt.title(method_name)
    plt.legend()
    plt.savefig(csv_file_path.replace(".csv", ".png"))
    plt.close()

def getImgIndex(img_path : str) -> int:
    index = img_path.split("/")[-1].split(".")[0].replace("im", '')
    return int(index)

def matchAll(frames_path, template_path, save_path, option_save_img):
    # Obtendo uma lista com o path de cada frame dentro do diretório frames_path:
    frame_paths = glob(f"{frames_path}/*")
    # Ordena os frames por índice:
    frame_paths = sorted(frame_paths, key=getImgIndex)

    template = cv.imread(template_path, cv.IMREAD_GRAYSCALE)
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    createDir(save_path)

    # Para construir uma tabela para cada método é necessário que os for's...
    # ... estejam nesta ordem:
    for meth in methods:
        # Note que memeth.split(".")[-1] retorna o nome do método sem "cv.":
        meth_save_path = os.path.join(save_path, meth.split(".")[-1])
        # Cria um diretório dentro da pasta com nome do método dentro do....
        # ... diretório save_path:
        createDir(meth_save_path)

        csv_file_path = os.path.join(meth_save_path, meth.split(".")[-1] + ".csv")
        csv_file = open(csv_file_path, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([meth])
        csv_writer.writerow(["name", "min_val", "max_val"])

        # Para cada imagem:
        for frame_path_name in frame_paths:
            img = cv.imread(frame_path_name, cv.IMREAD_GRAYSCALE)
            name = frame_path_name.split(".")[0].split("/")[-1]

            min_val, max_val = matchTemplate(meth, img, template, meth_save_path, name, option_save_img)
            csv_writer.writerow([name, min_val, max_val])

def saveFrame(video_path, save_dir):
    # Obtendo o nome do video (sem a extensão):
    name = video_path.split("/")[-1].split(".")[0]
    # Cria um diretório com o nome do video no diretório passado como argumento...
    # ... para salvar os frames:
    save_path = os.path.join(save_dir, "Frames " + "(" + name + ")")
    # Cria o diretório com o nome do vídeo caso ele não exista:
    createDir(save_path)

    index = 0
    video = cv.VideoCapture(video_path)
    while True:
        result, frame = video.read()

        if result == False:
            video.release()
            break

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Salve o frame no diretório com seu nome (save_path)
        cv.imwrite(f"{save_path}/im{index}.png", gray_frame)
        index += 1

def createAllTemplateVideos(path):
    results_path = glob(path)
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    
    fourcc = cv.VideoWriter_fourcc('M','J','P','G')

    for result_path in results_path:
        for method in methods:
            method_name = method.replace("cv.", "")
            save_path = result_path + "/" + method_name + "/"

            frames_path = glob(result_path + "/" + method_name + "/im*.png")
            frames_path = sorted(frames_path, key=getImgIndex)

            img_example = cv.imread(frames_path[0], cv.IMREAD_GRAYSCALE)
            w, h = (img_example.shape[1], img_example.shape[0])

            video_file = cv.VideoWriter(save_path + "video-teste-template.avi", fourcc, 30.0, (w, h), False)
            for frame_path in frames_path:
                frame = cv.imread(frame_path, cv.IMREAD_GRAYSCALE)
                video_file.write(frame)

            video_file.release()

if __name__ == "__main__":
    # Obtém todos os paths de cada video:
    video_paths = glob("Videos/*")
    # Diretório para salvar os frames de cada video:
    save_dir = "Frames"

    # Para cada video salvar os frames:
    for path in video_paths:
        # executa a função que gera uma pasta com os frames do vídeo:
        saveFrame(path, save_dir)

    # Obtém lista das pastas de frames de cada video:
    frames_paths = glob("Frames/*")
    # Pra cada pasta de frames:
    for path in frames_paths:
        # Quando isto é printado o usuário deve utilizar um frame do vídeo para gerar um template...
        # ... e o template deve estar no mesmo diretório deste código:
        print(f"Create template with {path} and type something when done: ")
        # Aperte 'enter' quando tiver feito o template:
        input()
        print("Loading...")
        # Obtém o nome do vídeo a partir de sua pasta de frames:
        sub_dir_name = path.split("/")[-1].split(" ")[-1].replace("(", "").replace(")", "")
        # Gera pasta com os frames após aplicação do algoritmo de rastreamento (dentro da pasta results):
        matchAll(path, "template.png", f"Results/Result ({sub_dir_name})", True)

    # Obtém todas as pastas de resultados relacionados aos frames de cada video:
    results_path = glob("Results/*")
    # Para os frames de resultado de cada video:
    for result_path in results_path:
        # Em cada pasta de resultados é criada uma pasta de resultados para cada método; aqui se obtém a lista destas...
        # ... relacionadas a um determinado video:
        methods_path = glob(result_path + "/*")
        # Na pasta de cade método:
        for method_path in methods_path:
            # Cria nome da tabela csv baseado no nome do método:
            method_csv_file = method_path.split("/")[-1]
            # Monta tabela csv e gráfico para o método:
            buildGraph(method_path + "/" + method_csv_file + ".csv")

    # Cria todos os vídeos com rastreamento usando os frames de cada video da pasta result:
    createAllTemplateVideos("Results/*")    
# Comando para criar video dentro da pasta com os frames do vídeo que se deseja montar:
# ffmpeg -framerate 30 -i im%d.png -pix_fmt yuv420p -r 30 video-with-template.mp4
