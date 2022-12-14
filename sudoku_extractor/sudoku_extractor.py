print('Setting UP')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
from os.path import join
exe_path = os.getcwd()
from copy import deepcopy
from tqdm import tqdm
from collections import Counter, defaultdict
#Tesseract Library
import pytesseract

#Warnings
import warnings
warnings.filterwarnings("ignore")

if 'projet_sudoku' in exe_path:
    exe_path = exe_path.split('projet_sudoku')[0]
if 'PROJETS' not in exe_path:
    exe_path = join(exe_path, "PROJETS")
if 'projet_sudoku' not in exe_path:
    exe_path = join(exe_path, "projet_sudoku")

sys.path.append(exe_path)
print(f"[sudoku_extractor] execution path= {exe_path}")
from sudoku_util import SUDOKUS, print_sudoku, EXECUTION_PATH, create_dir, remove_file_if_exist, get_sudoku_img_path, list_dir_files, most_number_by_idx, preProcess
# from sudoku_extractor_utils import *
from sudoku_extractor.sudoku_extractor_utils import *

########################################################################
  # LOAD THE CNN MODEL
########################################################################

class SudokuExtractor():

    heightImg = 450
    widthImg = 450
    models_path = [
                    r'C:\Users\User\WORK\workspace-ia\PROJETS\projet_sudoku\model\aurao-V2',
                    r'C:\Users\User\WORK\workspace-ia\PROJETS\projet_sudoku\sudoku_extractor\myModel.h5',
                    r'C:\Users\User\WORK\workspace-ia\PROJETS\projet_sudoku\model\aurao-V3',
                ]

    def __init__(self,heightImg = 450,widthImg = 450, models=None, verbose=0):
        short_name = "SudokuExtractor.contructor"
        self.verbose=verbose
        self.heightImg = heightImg
        self.widthImg = widthImg
        if models is None:
            self.models = {}
            for path in self.models_path:
                mod = intializePredectionModel(model_path=path, verbose=self.verbose)
                if mod is not None:
                    mod_name = path.split('\\')[-1]
                    mod_name = mod_name.split('/')[-1]
                    self.models[mod_name] = mod
                    if self.verbose>1:
                        print(f"[{short_name}]\tDEBUG : model {path}     LOAD")
        else:
            self.models = models

    def blank_img():
        imgBlank = np.zeros((SudokuExtractor.heightImg, SudokuExtractor.widthImg, 3), np.uint8)  
        return imgBlank

    def sudoku_matrice(self, pathImage):
        m = None
        boxes = self.extract_sudoku_img(pathImage=pathImage)
        if boxes is not None:
            m = self.predict_sudoku_number(boxes=boxes)
        return m

    def extract_sudoku_img(self, pathImage):
        short_name = "SudokuExtractor.extract_sudoku_img"
        boxes = None
        #### 1. PREPARE THE IMAGE
        img = cv2.imread(pathImage)

        if img is not None:
            img = cv2.resize(img, (self.widthImg, self.heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
            imgThreshold = preProcess(img_path=pathImage, size=(self.widthImg, self.heightImg), verbose=self.verbose-1)
            
            # #### 2. FIND ALL COUNTOURS
            contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
            
            #### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
            biggest, _ = biggestContour(contours) # FIND THE BIGGEST CONTOUR
            if self.verbose>1:
                print(f"[{short_name}]\tDEBUG : {biggest}")

            if biggest.size != 0:
                biggest = reorder(biggest)
                if self.verbose>1:
                    print(f"[{short_name}]\tDEBUG : {biggest}")
                
                pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
                pts2 = np.float32([[0, 0],[self.widthImg, 0], [0, self.heightImg],[self.widthImg, self.heightImg]]) # PREPARE POINTS FOR WARP
                matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
                imgWarpColored = cv2.warpPerspective(img, matrix, (self.widthImg, self.heightImg))
                imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

                #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
                boxes = splitBoxes(imgWarpColored)
                if self.verbose>1:
                    print(f"[{short_name}]\tDEBUG : {len(boxes)} boxes")
            else:
                if self.verbose>0:
                    print(f"[{short_name}]\tINFO : No Sudoku Found for {pathImage}")
        return boxes

    def predict_sudoku_number(self, boxes):
        short_name = "SudokuExtractor.predict_sudoku_number"
        board = None
        diff_boxes_idx = []
        if boxes is not None:
            if self.verbose>1:
                print(f"[{short_name}]\tDEBUG : {len(boxes)} boxes")
                print(f"[{short_name}]\tDEBUG : model loading....", end="")
            
            numbers_by_models = {}
            for model_name, model in self.models.items():
                numbers1 = getPredection(boxes, model, verbose=self.verbose)
                if self.verbose>1:
                    print(f"[{short_name}]\tDEBUG : {numbers1}")
                numbers_by_models[model_name] = numbers1           

            # Comparaison entre les models
            numbers, diff_boxes_idx, diff_model = most_number_by_idx(numbers_by_models, verbose=self.verbose)
            
            # D??paratage des models via un 3??me uniquement sur les images en d??saccord
            if len(diff_boxes_idx)>0:
                if self.verbose>0:
                    print(f"[{short_name}]\tINFO : {len(diff_boxes_idx)} differences between models, trying with ocs...")
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                diff_boxes_idx3 = []
                for idx in diff_boxes_idx:
                    num = pytesseract.image_to_string(boxes[idx],config=r'--oem 3 --psm 6 outputbase digists')
                    num = num.strip()
                    found = False
                    for model_name in numbers_by_models.keys():
                        mod_num = numbers_by_models[model_name][idx]
                        if str(mod_num) in num:
                            numbers[idx] = mod_num
                            found = True
                            break
                    
                    if not found:
                        diff_boxes_idx3.append(idx)
                        numbers[idx] = 0

                if self.verbose>0:
                    print(f"[{short_name}]\tINFO : {len(diff_boxes_idx3)} reminded differences between models and ocs")

            board = np.array_split(numbers,9)
        else:
            if self.verbose>0:
                print(f"[{short_name}]\tINFO : no boxe received")

        return board
        
# ----------------------------------------------------------------------------------
#  %%                      TEST
# ----------------------------------------------------------------------------------
def _test_SudokuExtractor(verbose=1):
    short_name = "sudoku_extractor"
    to_test = deepcopy(get_sudoku_img_path(verbose=verbose))
    verbose = 0
    extractor = SudokuExtractor(verbose=verbose)
    fails_files = {}
    nb_occu = Counter()

    for img_path in tqdm(to_test, desc=short_name):
        file_name = img_path.split('/')[-1]
        file_name = file_name.split('\\')[-1]
        boxes = extractor.extract_sudoku_img(pathImage=img_path)
        if boxes is not None:
            predic = np.array(extractor.predict_sudoku_number(boxes=boxes))
            expected = np.array(SUDOKUS.get(file_name, []))
            nb_occu = Counter(expected.flatten()) + nb_occu
            
            if np.array_equal(predic, expected) :
                assert True
            else:
                print(f"[{short_name}]\tFAIL : {file_name} => prediction FAIL")
                fails_files[file_name] = predic
        else:
            print(f"[{short_name}]\tFAIL : {file_name} => no boxes")
        
    if len(fails_files) >0:
        fail_number = {}
        what_fail = defaultdict(list)
        for file_name, predic in fails_files.items():
            expected = SUDOKUS.get(file_name, [])
            for i in range(0,9):
                for j in range(0,9):
                    if predic[i][j] != expected[i][j]:
                        fail_number[expected[i][j]] = fail_number.get(expected[i][j], 0)+1
                        what_fail[expected[i][j]].append(predic[i][j])
            print("-------------------------------------------------------------------------------")
            print(file_name, "PREDICT : ")
            print_sudoku(predic)
            print(file_name, "EXPECTED : ")
            print_sudoku(expected)
            print("-------------------------------------------------------------------------------")

        fail_number = Counter(fail_number)
        
        frequency = {}
        for _ ,val in enumerate(nb_occu.most_common()):
            frequency[val[0]] = val[1]

        # avec uniquement le model 1 :
        # FAIL NUMBERS :  [(3, 7), (8, 6), (5, 3), (7, 3), (9, 2), (1, 1), (4, 1), (6, 1)]
        # 3 = 7 fails on 27 (0.26) => [(2, 4), (0, 2), (8, 1)]
        # 8 = 6 fails on 33 (0.18) => [(2, 2), (6, 2), (4, 1), (0, 1)]
        # 5 = 3 fails on 34 (0.09) => [(0, 3)]
        # 7 = 3 fails on 29 (0.1)  => [(1, 2), (0, 1)]
        # 9 = 2 fails on 25 (0.08) => [(8, 2)]
        # 1 = 1 fails on 35 (0.03) => [(7, 1)]
        # 4 = 1 fails on 23 (0.04) => [(6, 1)]
        # 6 = 1 fails on 33 (0.03) => [(1, 1)]
        print("FAIL NUMBERS : ", fail_number.most_common())
        for _ ,val in enumerate(fail_number.most_common()):
            key = val[0]
            nb = val[1]
            print(f"{key} = {nb} fails on {frequency.get(key)} ({round(nb/frequency.get(key), 2)}) => {Counter(what_fail.get(key)).most_common()}")
        
            
        assert False, f"[{short_name}]\t FAIL on {len(fails_files)}/{len(to_test)} files : {fails_files.keys()} : "

def _test_boxes(verbose=1):
    short_name = "_test_boxes"
   
    # to_test = deepcopy(get_sudoku_img_path(verbose=verbose))

    dir_path = join(EXECUTION_PATH, "dataset", "to_boxes")
    to_test = list_dir_files(dir_path=dir_path, verbose=verbose)

    verbose = 0
    extractor = SudokuExtractor(verbose=verbose)
    
    for img_path in tqdm(to_test, desc=short_name):
        file_name = img_path.split('/')[-1]
        file_name = file_name.split('\\')[-1]
        boxes = extractor.extract_sudoku_img(pathImage=img_path)
        if boxes is not None:
            dest_path = join(dir_path, file_name[:-4])
            remove_file_if_exist(dest_path,  backup_file=False, verbose=verbose)
            create_dir(dest_path,verbose=verbose)
            i = 0
            for box in boxes:
                i += 1
                dest = join(dest_path, file_name.replace(".png", "-"+str(i)+".png"))
                cv2.imwrite(dest, box)

# ----------------------------------------------------------------------------------
#                        MAIN
# ----------------------------------------------------------------------------------
# %% main
if __name__ == '__main__':
    short_name = "sudoku_extractor"
    _test_boxes()
    # _test_SudokuExtractor()



