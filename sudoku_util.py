
# ----------------------------------------------------------------------------------
#  %%                      CONSTANTS
# ----------------------------------------------------------------------------------
from collections import Counter, defaultdict
from os import getcwd
from os.path import join
import numpy as np 
import cv2 
from matplotlib import pyplot as plt

EXECUTION_PATH = getcwd()

if 'projet_sudoku' in EXECUTION_PATH:
    EXECUTION_PATH = EXECUTION_PATH.split('projet_sudoku')[0]
if 'PROJETS' not in EXECUTION_PATH:
    EXECUTION_PATH = join(EXECUTION_PATH, "PROJETS")
if 'projet_sudoku' not in EXECUTION_PATH:
    EXECUTION_PATH = join(EXECUTION_PATH, "projet_sudoku")
print(f"[sudoku_util] execution path= {EXECUTION_PATH}")


PATH_SUDOKU_DIR = join(EXECUTION_PATH, "dataset", "sudoku")

# SUDOKU_IMG_PATH = list({join(EXECUTION_PATH, "dataset", "sudoku-00"+str(i)+".png") for i in range(1, 9)} | {join(EXECUTION_PATH, "dataset", "sudoku-0"+str(i)+".png") for i in range(10, 20)} )

SUDOKUS = { 
            "sudoku-001.png" :[ [5,3,0,0,7,0,0,0,0],
                                [6,0,0,1,9,5,0,0,0],
                                [0,9,8,0,0,0,0,6,0],

                                [8,0,0,0,6,0,0,0,3],
                                [4,0,0,8,0,3,0,0,1],
                                [7,0,0,0,2,0,0,0,6],

                                [0,6,0,0,0,0,2,8,0],
                                [0,0,0,4,1,9,0,0,5],
                                [0,0,0,0,8,0,0,7,9],
                            ],

            "sudoku-002.png" :[ [0,0,0,0,0,0,0,0,0],
                                [0,1,2,0,3,4,5,6,7],
                                [0,3,4,5,0,6,1,8,2],

                                [0,0,1,0,5,8,2,0,6],
                                [0,0,8,6,0,0,0,0,1],
                                [0,2,0,0,0,7,0,5,0],

                                [0,0,3,7,0,5,0,2,8],
                                [0,8,0,0,6,0,7,0,0],
                                [2,0,7,0,8,3,6,1,5],
                            ],
        
            "sudoku-003.png" : [[2,0,9,0,0,0,6,0,0],
                        [0,4,0,8,7,0,0,1,2],
                        [8,0,0,0,1,9,0,4,0],
                        [0,3,0,7,0,0,8,0,1],
                        [0,6,5,0,0,8,0,3,0],
                        [1,0,0,0,3,0,0,0,7],
                        [0,0,0,6,5,0,7,0,9],
                        [6,0,4,0,0,0,0,2,0],
                        [0,8,0,3,0,1,4,5,0]],

            "sudoku-004.png" :[[1,0,0,0,8,0,0,0,9],
                        [0,5,0,6,0,1,0,2,0],
                        [0,0,0,5,0,3,0,0,0],
                        
                        [0,9,6,1,0,4,8,3,0],
                        [3,0,0,0,6,0,0,0,5],
                        [0,1,5,9,0,8,4,6,0],

                        [0,0,0,7,0,5,0,0,0],
                        [0,8,0,3,0,9,0,7,0],
                        [5,0,0,0,1,0,0,0,3],
            ],

            "sudoku-005.png" :[[0,0,5,0,0,0,8,0,0],
                        [8,1,6,0,0,5,4,2,7],
                        [7,0,2,6,0,0,0,1,9],
                        
                        [2,0,0,0,0,7,3,0,1],
                        [6,9,0,1,0,8,7,0,0],
                        [3,7,1,5,0,0,0,4,0],

                        [0,6,0,9,0,2,0,0,0],
                        [1,0,3,0,4,0,9,7,0],
                        [5,8,0,7,0,0,2,6,4],
            ],

            "sudoku-006.png" :[ [8,0,0,0,0,0,0,0,0],
                                [0,0,3,6,0,0,0,0,0],
                                [0,7,0,0,9,0,2,0,0],

                                [0,5,0,0,0,7,0,0,0],
                                [0,0,0,0,4,5,7,0,0],
                                [0,0,0,1,0,0,0,3,0],

                                [0,0,1,0,0,0,0,6,8],
                                [0,0,8,5,0,0,0,1,0],
                                [0,9,0,0,0,0,4,0,0],
                            ],
            
            "sudoku-007.png" :[ [2,1,0,0,6,0,9,0,0],
                                [0,0,0,0,0,9,1,0,0],
                                [4,0,9,3,1,0,0,5,8],

                                [0,0,1,0,0,5,0,4,0],
                                [9,0,4,0,3,0,8,0,5],
                                [0,5,0,2,0,0,6,0,0],

                                [3,8,0,0,4,0,5,0,6],
                                [0,0,6,7,0,0,0,0,2],
                                [0,0,7,0,8,0,3,0,9],
                            ],

            "sudoku-008.png" :[ [0,4,0,2,0,1,0,6,0],
                                [0,0,0,0,0,0,0,0,0],
                                [9,0,5,0,0,0,3,0,7],

                                [0,0,0,0,0,0,0,0,0],
                                [5,0,7,0,8,0,1,0,4],
                                [0,1,0,0,0,0,0,9,0],

                                [0,0,1,0,0,0,6,0,0],
                                [0,0,0,7,0,5,0,0,0],
                                [6,0,8,9,0,4,5,0,3],
                            ],
    }

SUDOKUS_ANSWER = { 
           "sudoku-003.png" : [[2,1,9,5,4,3,6,7,8],
                        [5,4,3,8,7,6,9,1,2],
                        [8,7,6,2,1,9,3,4,5],
                        [4,3,2,7,6,5,8,9,1],
                        [7,6,5,1,9,8,2,3,4],
                        [1,9,8,4,3,2,5,6,7],
                        [3,2,1,6,5,4,7,8,9],
                        [6,5,4,9,8,7,1,2,3],
                        [9,8,7,3,2,1,4,5,6]],

            "sudoku-005.png" :[[9,4,5,2,7,1,8,3,6],
                        [8,1,6,3,9,5,4,2,7],
                        [7,3,2,6,8,4,5,1,9],
                        
                        [2,5,8,4,6,7,3,9,1],
                        [6,9,4,1,3,8,7,5,2],
                        [3,7,1,5,2,9,6,4,8],

                        [4,6,7,9,5,2,1,8,3],
                        [1,2,3,8,4,6,9,7,5],
                        [5,8,9,7,1,3,2,6,4],
            ],
            # "sudoku-004.png" :[[1,3,7,4,8,2,6,5,9],
            #             [8,5,9,6,7,1,3,2,4],
            #             [6,2,4,5,9,3,7,8,1],

            #             [2,9,6,1,5,4,8,3,7],
            #             [3,4,8,2,6,7,1,9,5],
            #             [7,1,5,9,3,8,4,6,2],
                        
            #             [9,6,3,7,4,5,2,1,8],
            #             [4,8,1,3,2,9,5,7,6],
            #             [5,7,2,8,1,6,9,4,3]],

            # "sudoku-004.pngb":[[1, 6, 3, 4, 8, 2, 7, 5, 9],
            #             [9, 5, 4, 6, 7, 1, 3, 2, 8],
            #             [8, 2, 7, 5, 9, 3, 6, 1, 4],

            #             [2, 9, 6, 1, 5, 4, 8, 3, 7],
            #             [3, 4, 8, 2, 6, 7, 1, 9, 5],
            #             [7, 1, 5, 9, 3, 8, 4, 6, 2],

            #             [4, 3, 1, 7, 2, 5, 9, 8, 6],
            #             [6, 8, 2, 3, 4, 9, 5, 7, 1],
            #             [5, 7, 9, 8, 1, 6, 2, 4, 3]],
    }
# ----------------------------------------------------------------------------------
#  %%                      FILES
# ----------------------------------------------------------------------------------
from pathlib import Path
def create_dir(dest_path, verbose=0):
    """
    Create dir

    Args:
        dest_path (str): destination path (directory)
        verbose (int, optional): log level. Defaults to 0.
    """
    # Création du répertoire s'il n'existe pas
    if dest_path is None or len(dest_path.strip()) > 0:   
        base = Path(dest_path)
        base.mkdir(exist_ok=True)
        
    return dest_path

from os.path import join, exists, isfile
from os import remove, rename
import shutil

def remove_file_if_exist(file_path, backup_file=False, verbose=0):
    """
    Remove file

    Args:
        file_path (str): the file path (inlude file name)
        backup_file (bool, optional): if True save the previous file with .backup. Defaults to False.
        verbose (int, optional): Log level. Defaults to 0.
    """
    if (exists(file_path)):
        if isfile(file_path):
            if backup_file:
                if (exists(str(file_path)+".backup")):
                    remove(str(file_path)+".backup")
                rename(str(file_path), str(file_path)+".backup")
            else:
                try:
                    remove(file_path)
                except Exception as error:
                    shutil.rmtree(file_path)
        else:
            shutil.rmtree(file_path)

from glob import glob
def list_dir_files(dir_path, endwith=None, verbose=0):
    end = "*"
    if endwith is not None:
        end = endwith.replace(".", "")

    files = glob(f"{dir_path}/*.{end}")
    return files

def list_dir_dir(dir_path, verbose=0):
    li_dir = []
    files = glob.glob(f"{dir_path}")
    for f in files:
        if not isfile(f):
            li_dir.append(f)

    return li_dir
# ----------------------------------------------------------------------------------
#  %%                      IMAGES
# ----------------------------------------------------------------------------------
import cv2
from copy import deepcopy
def preProcess(img_path, size = None, less_limit=200,verbose=0):
    res = None
    t_img = cv2.imread(img_path,0) 
    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    noiseless_image_bw = cv2.fastNlMeansDenoising(t_img, None, 20, 7, 21) 
    imgBlur = cv2.GaussianBlur(noiseless_image_bw, (5, 5), 1)  # ADD GAUSSIAN BLUR

    # imgReduc = deepcopy(imgBlur)
    # if less_limit is not None:
    #     for i in range(0, len(imgBlur)):
    #         for j in range(0, len(imgBlur[i])):
    #             if imgBlur[i][j] < less_limit:
    #                 imgReduc[i][j] = 0
    #             else:
    #                 imgReduc[i][j] = 255
    
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)  # APPLY ADAPTIVE THRESHOLD
    res = imgThreshold
    # imgThresholdReduce = None
    # if less_limit is not None:
    #     imgThresholdReduce = cv2.adaptiveThreshold(imgReduc, 255, 1, 1, 11, 2)  # APPLY ADAPTIVE THRESHOLD
    #     res = imgThresholdReduce
    
    if size is not None:
        res = cv2.resize(res, size) 
    
    if verbose>0:
        images = {
            'Orignial B&W':t_img,
            'noiseless' : noiseless_image_bw,
            'GaussianBlur' : imgBlur, 
            'adaptiveThreshold' : imgThreshold,
            }
        # if len(imgReduc)>0:
        #     images["imgReduc"] = imgReduc
        #     images["imgThresholdReduce"] = imgThresholdReduce
        displayImages(images=images)
    return res


def displayImages(images):
    
    plt.figure(figsize=(13,3))
    i = 0
    for title, img in images.items():
        plt.subplot(1,len(images),i+1)
        plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.xticks([])
        plt.yticks([])
        i += 1
    plt.tight_layout()
    plt.show()

def draw_digits(X, y=None, nb=None):
    
    # plot some of the numbers
    if nb is None:
        nb = len(X)

    nb_cols = 10
    nb_lignes = (nb//nb_cols)

    plt.figure(figsize=(14,(nb_lignes*1.5)))
    for digit_num in range(0,nb):
        plt.subplot(nb_lignes,nb_cols,digit_num+1)
        grid_data = X[digit_num].reshape(28,28)  # reshape from 1d to 2d pixel array
        plt.imshow(grid_data, interpolation = "none", cmap = "afmhot")
        if y is not None:
            plt.title(y[digit_num])
        plt.axis("off")
    plt.tight_layout()
    plt.show()

# ----------------------------------------------------------------------------------
#  %%                      SUDOKU
# ----------------------------------------------------------------------------------
def print_sudoku(grille):
    """ display the grid like :
    -------------------------------------
    | 2 :   : 9 |   :   :   | 6 :   :   |
    |   : 4 :   | 8 : 7 :   |   : 1 : 2 |
    | 8 :   :   |   : 1 : 9 |   : 4 :   |
    -------------------------------------
    |   : 3 :   | 7 :   :   | 8 :   : 1 |
    |   : 6 : 5 |   :   : 8 |   : 3 :   |
    | 1 :   :   |   : 3 :   |   :   : 7 |
    -------------------------------------
    |   :   :   | 6 : 5 :   | 7 :   : 9 |
    | 6 :   : 4 |   :   :   |   : 2 :   |
    |   : 8 :   | 3 :   : 1 | 4 : 5 :   |
    -------------------------------------

    Args:
        grille (list(list), optional): _description_. Defaults to None.
    """
    if grille is not None:
        print("-------------------------------------")
        for i in range(9):
            print(f"|", end="")
            for j in range(9):
                val = grille[i][j] if grille[i][j] > 0 else " "
                sep = "|" if j in [2,5,8] else ":"
                print(f" {val} {sep}", end="")
            print("")
            if i in [2,5,8]:
                print("-------------------------------------")
    else:
        print("Nothing to display")


def print_sudoku_and_result(grille, grille_result):
    """ display the grid like :
    -------------------------------------   -------------------------------------
    | 5 : 3 :   |   : 7 :   |   :   :   |   | 5 : 3 : 4 | 6 : 7 : 8 | 9 : 1 : 2 |
    | 6 :   :   | 1 : 9 : 5 |   :   :   |   | 6 : 7 : 2 | 1 : 9 : 5 | 3 : 4 : 8 |
    |   : 9 : 8 |   :   :   |   : 6 :   |   | 1 : 9 : 8 | 3 : 4 : 2 | 5 : 6 : 7 |
    -------------------------------------   -------------------------------------
    | 8 :   :   |   : 6 :   |   :   : 3 |   | 8 : 5 : 9 | 7 : 6 : 1 | 4 : 2 : 3 |
    | 4 :   :   | 8 :   : 3 |   :   : 1 |   | 4 : 2 : 6 | 8 : 5 : 3 | 7 : 9 : 1 |
    | 7 :   :   |   : 2 :   |   :   : 6 |   | 7 : 1 : 3 | 9 : 2 : 4 | 8 : 5 : 6 |
    -------------------------------------   -------------------------------------
    |   : 6 :   |   :   :   | 2 : 8 :   |   | 9 : 6 : 1 | 5 : 3 : 7 | 2 : 8 : 4 |
    |   :   :   | 4 : 1 : 9 |   :   : 5 |   | 2 : 8 : 7 | 4 : 1 : 9 | 6 : 3 : 5 |
    |   :   :   |   : 8 :   |   : 7 : 9 |   | 3 : 4 : 5 | 2 : 8 : 6 | 1 : 7 : 9 |
    -------------------------------------   -------------------------------------

    Args:
        grille (list(list), optional): _description_. Defaults to None.
    """
    if grille is not None:
        print("-------------------------------------\t-------------------------------------")
        for i in range(9):
            print(f"|", end="")
            for j in range(9):
                val = grille[i][j] if grille[i][j] > 0 else " "
                sep = "|" if j in [2,5,8] else ":"
                print(f" {val} {sep}", end="")
            print('\t|', end="")
            for j in range(9):
                val = grille_result[i][j] if grille_result[i][j] > 0 else " "
                sep = "|" if j in [2,5,8] else ":"
                print(f" {val} {sep}", end="")
            grille_result
            print("")
            if i in [2,5,8]:
                print("-------------------------------------\t-------------------------------------")
    else:
        print("Nothing to display")

def get_sudoku_img_path(verbose=0):
    res = []
    sudoku_files = list_dir_files(dir_path=PATH_SUDOKU_DIR, endwith=".png", verbose=verbose)
    for f in sudoku_files:
        if "answer" not in f:
            res.append(f)
    return res

def most_number_by_idx(numbers_by_key, verbose=0):
    short_name = "converge_most_number_by_idx"
    # Comparaison des mdoèles
    numbers = []
    diff_boxes_idx = []
    diff_model = []
    keys = list(numbers_by_key.keys())
    first = numbers_by_key.get(keys[0], [])
    
    numbers_by_idx = defaultdict(list)

    for n in range(len(first)):
        for k in keys:
            numbers_by_idx[n].append(numbers_by_key.get(k, [])[n])
        count_val_for_idx = Counter(numbers_by_idx[n])
        maxi = count_val_for_idx.most_common()[0]
        if maxi[1] == len(keys):
            numbers.append(maxi[0])
        elif maxi[1] > 1 and maxi[1]>count_val_for_idx.most_common()[1][1]:
            numbers.append(maxi[0])
        else:
            numbers.append(0)
            diff_model.append(count_val_for_idx.most_common())
            diff_boxes_idx.append(n)
   
    return numbers, diff_boxes_idx, diff_model

# ----------------------------------------------------------------------------------
#                        TEST
# ----------------------------------------------------------------------------------
def _test_most_number_by_idx(verbose=1):
    numbers_by_key = {
        "model1" : [0,1,2,3,4,5,6,7,8,9],
        "model2" : [0,1,3,3,4,5,8,7,8,9],
        "model3" : [1,1,2,3,4,5,9,7,8,9],
    }

    expected = [0,1,2,3,4,5,0,7,8,9]

    numbers, diff_boxes_idx = most_number_by_idx(numbers_by_key=numbers_by_key, verbose=verbose)
    assert numbers == expected

# ----------------------------------------------------------------------------------
#                        MAIN
# ----------------------------------------------------------------------------------
# %% main
if __name__ == '__main__':
    short_name = "sudoku_util"

    _test_most_number_by_idx()

    print_sudoku(SUDOKUS.get("sudoku-008.png", []))

    print_sudoku_and_result(SUDOKUS.get("sudoku-008.png", []), SUDOKUS.get("sudoku-008.png", []))