print('Setting UP')
import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
from os.path import join
exe_path = os.getcwd()
from copy import deepcopy
from tqdm import tqdm
import numpy as np
from datetime import datetime
import cv2
if 'PROJETS' not in exe_path:
    exe_path = join(exe_path, "PROJETS")
if 'projet_sudoku' not in exe_path:
    exe_path = join(exe_path, "projet_sudoku")

print(f"[sudoku_demonstrator] execution path= {exe_path}")
sys.path.append(exe_path)
from sudoku_util import SUDOKU_IMG_PATH, print_sudoku_and_result, print_sudoku
from sudoku_extractor.sudoku_extractor import SudokuExtractor
from sudoku_extractor.sudoku_extractor_utils import *
from sudoku_solver.suduko_solver_recurcif import solve


def display_result(pathImage, grille_src, board, verbose=0):
    
    heightImg = 450
    widthImg = 450
   
    #### 1. PREPARE THE IMAGE
    img = cv2.imread(pathImage)
    img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgThreshold = preProcess(img)

    # #### 2. FIND ALL COUNTOURS
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS

    #### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
    biggest, _ = biggestContour(contours) # FIND THE BIGGEST CONTOUR
    if verbose>1: print(biggest)
    if biggest.size != 0:
        biggest = reorder(biggest)
        if verbose>1: print(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgDetectedDigits = imgBlank.copy()
        imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

        #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
        
        imgDetectedDigits = displayNumbers(imgDetectedDigits, grille_src, color=(255, 0, 255))
        grille_src = np.asarray(grille_src)
        posArray = np.where(grille_src > 0, 0, 1)
        if verbose>1: print_sudoku(posArray)
        if verbose>0: print_sudoku_and_result(grille_src, board)

        flatList = np.array(board)
        flatList = flatList.flatten()

        flatpos = np.array(posArray)
        flatpos = flatpos.flatten()
        
        solvedNumbers =flatList*flatpos

        imgSolvedDigits = imgBlank.copy()
        imgSolvedDigits= displayNumbers(imgSolvedDigits,solvedNumbers)

        # #### 6. OVERLAY SOLUTION
        pts2 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts1 =  np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
        imgInvWarpColored = img.copy()
        imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
        inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
        imgDetectedDigits = drawGrid(imgDetectedDigits)
        imgSolvedDigits = drawGrid(imgSolvedDigits)

        # imageArray = ([img,imgThreshold,imgContours, imgBigContour],
        #             [imgDetectedDigits, imgSolvedDigits,imgInvWarpColored,inv_perspective])
        imageArray = ([img, inv_perspective])
        if verbose>1:
            imageArray = ([img, imgDetectedDigits],
                        [imgSolvedDigits,inv_perspective])
        stackedImage = stackImages(imageArray, 1)
        cv2.imshow('Stacked Images', stackedImage)

    else:
        print("No Sudoku Found")

    cv2.waitKey(0)

# ----------------------------------------------------------------------------------
#  %%                      TEST
# ----------------------------------------------------------------------------------
def resolve_sudoku(img_path, verbose=1):
    short_name = "resolve_sudoku"
    now = datetime.now() # current date and time
    grille = None
    bo = None
    file_name = img_path.split('/')[-1]
    file_name = file_name.split('\\')[-1]

    extractor = SudokuExtractor(verbose=verbose-1)
    grille = extractor.sudoku_matrice(pathImage=img_path)
    if verbose>0:
        print(f"[{short_name}]\tINFO : extraction {file_name} in : {datetime.now()-now}")

    if grille is not None:
        step2 = datetime.now() # current date and time
        bo = deepcopy(grille)
        solve(bo)
        print_sudoku_and_result(grille, bo)
    if verbose>0:
        print(f"[{short_name}]\tINFO : solve {file_name} in : {datetime.now()-step2}")
        print(f"[{short_name}]\tINFO : complete {file_name} in : {datetime.now()-now}")
    return grille, bo
    
    

# ----------------------------------------------------------------------------------
#                        MAIN
# ----------------------------------------------------------------------------------
# %% main
if __name__ == '__main__':
    short_name = "sudoku_extractor"
    verbose = 1
    for img_path in SUDOKU_IMG_PATH:
        print(f"[{short_name}]\tINFO : {img_path}")
        grille_src, board = resolve_sudoku(img_path=img_path, verbose=verbose)
        if grille_src is not None and board is not None:
            display_result(pathImage=img_path, grille_src=grille_src, board=board, verbose=verbose)
            print("")
