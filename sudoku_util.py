
# ----------------------------------------------------------------------------------
#  %%                      CONSTANTS
# ----------------------------------------------------------------------------------
from os import getcwd
from os.path import join
execution_path = getcwd()

if 'PROJETS' not in execution_path:
    execution_path = join(execution_path, "PROJETS")
if 'projet_sudoku' not in execution_path:
    execution_path = join(execution_path, "projet_sudoku")
print(f"[sudoku_util] execution path= {execution_path}")

SUDOKU_IMG_PATH = [join(execution_path, "datase", "sudoku-00"+str(i)+".png") for i in range(1, 9)]        

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
#  %%                      FUNCTION
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

# ----------------------------------------------------------------------------------
#                        MAIN
# ----------------------------------------------------------------------------------
# %% main
if __name__ == '__main__':
    short_name = "sudoku_util"
    print_sudoku(SUDOKUS.get("sudoku-008.png", []))