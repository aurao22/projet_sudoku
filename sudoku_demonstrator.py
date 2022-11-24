
print('Setting UP')
import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
from os.path import join
exe_path = os.getcwd()
from copy import deepcopy
from tqdm import tqdm
from datetime import datetime

if 'PROJETS' not in exe_path:
    exe_path = join(exe_path, "PROJETS")
if 'projet_sudoku' not in exe_path:
    exe_path = join(exe_path, "projet_sudoku")

print(f"[sudoku_demonstrator] execution path= {exe_path}")
sys.path.append(exe_path)
from sudoku_util import SUDOKU_IMG_PATH, print_sudoku_and_result
from sudoku_extractor.sudoku_extractor import SudokuExtractor
from sudoku_solver.suduko_solver_recurcif import solve
      
# ----------------------------------------------------------------------------------
#  %%                      TEST
# ----------------------------------------------------------------------------------
def resolve_sudoku(img_path, verbose=1):
    short_name = "resolve_sudoku"
    now = datetime.now() # current date and time
    
    file_name = img_path.split('/')[-1]
    file_name = file_name.split('\\')[-1]
    extractor = SudokuExtractor(verbose=verbose-1)
    grille = extractor.sudoku_matrice(pathImage=img_path)
    if grille is not None:
        bo = deepcopy(grille)
        solve(bo)
        print_sudoku_and_result(grille, bo)

    if verbose>0:
        print(f"[{short_name}]\tINFO : resolve {file_name} in : {datetime.now()-now}")


# ----------------------------------------------------------------------------------
#                        MAIN
# ----------------------------------------------------------------------------------
# %% main
if __name__ == '__main__':
    short_name = "sudoku_extractor"

    for img_path in SUDOKU_IMG_PATH:
        resolve_sudoku(img_path=img_path, verbose=1)
