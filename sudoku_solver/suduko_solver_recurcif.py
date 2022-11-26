"""
This module finds the solution of a given sudoku problem
Code credits: Tim Ruscica
More info: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
Example input board
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]
"""
from datetime import datetime
from copy import deepcopy
import numpy as np
from tqdm import tqdm
import sys
from os import getcwd
from os.path import join
exe_path = getcwd()

if 'projet_sudoku' in exe_path:
    exe_path = exe_path.split('projet_sudoku')[0]
if 'PROJETS' not in exe_path:
    exe_path = join(exe_path, "PROJETS")
if 'projet_sudoku' not in exe_path:
    exe_path = join(exe_path, "projet_sudoku")
sys.path.append(exe_path)
print(f"[sudoku_solver_recurcif] execution path= {exe_path}")

from sudoku_util import print_sudoku, SUDOKUS, SUDOKUS_ANSWER

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0
    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False
    return True

def print_board(bo):
    print_sudoku(bo)

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None


# ----------------------------------------------------------------------------------
#  %%                      TEST
# ----------------------------------------------------------------------------------
def _test_sudoku_solver(verbose=1):
    short_name = "Test_suduko_solver_recurcif"
    execution_time = []

    for key, expected in tqdm(SUDOKUS_ANSWER.items(), desc=short_name):
        grille = SUDOKUS.get(key, None)
        if grille is not None:
            now = datetime.now() # current date and time
            bo = deepcopy(grille)
            if verbose>0:
                print_sudoku(bo)
            solve(bo)
            execution_time.append(datetime.now()-now)
            assert bo == expected
    # 0:00:00.009179 => 2 sudokus
    print(np.mean(execution_time))

    
# ----------------------------------------------------------------------------------
#                        MAIN
# ----------------------------------------------------------------------------------
# %% main
if __name__ == '__main__':
    short_name = "suduko_solver_recurcif"
    _test_sudoku_solver()

