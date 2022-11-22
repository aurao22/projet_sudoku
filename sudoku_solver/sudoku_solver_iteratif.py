# %% doc
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module to test the OpenCV library

Project: Sudoku
=======

Usage:
======
    python sudoku_solver.py
"""
__authors__     = ("Aurélie RAOUL")
__contact__     = ("aurelie.raoul@yahoo.fr")
__copyright__   = "MIT"
__date__        = "2022-11-22"
__version__     = "1.0.0"

from datetime import datetime, timedelta
from copy import deepcopy
import numpy as np
from tqdm import tqdm
from sudoku_util import print_sudoku, SUDOKUS, SUDOKUS_ANSWER

# ----------------------------------------------------------------------------------
#  %%                      CLASSES
# ----------------------------------------------------------------------------------
# Moteur de resolution
class SudokuSolver():
    
    def __init__(self, grille, verbose=0):
        if grille is not None:
            self.grille = deepcopy(grille)
        else:
            self.grille = [[0]*9 for n in range(9)]

        self.grilleFinie = [[False]*9 for n in range(9)]
        self.verbose=verbose
        
    def solutions(self, l,c,ites):
        short_name = "SudokuSolver.solutions()"
        self.verifier()
       
        lc = l in [0,1,2] and [0,1,2] or l in [3,4,5] and [3,4,5] or l in [6,7,8] and [6,7,8]
        cc = c in [0,1,2] and [0,1,2] or c in [3,4,5] and [3,4,5] or c in [6,7,8] and [6,7,8]
       
        # Methode de recherche : Inclusion
        if not self.grilleFinie[l][c]:
            if self.verbose>1:
                print(f"[{short_name}]\tDEBUG : Methode de recherche : Inclusion.....", end="")
            if not ites:
                self.grille[l][c] = [1,2,3,4,5,6,7,8,9]
            for k in range(9):
                if self.grilleFinie[l][k] and self.grille[l][k] in self.grille[l][c] and k != c:
                    self.grille[l][c].remove(self.grille[l][k])
                if self.grilleFinie[k][c] and self.grille[k][c] in self.grille[l][c] and k != l:
                    self.grille[l][c].remove(self.grille[k][c])
            for i in lc:
                for j in cc:
                    if self.grilleFinie[i][j] and self.grille[i][j] in self.grille[l][c] and (i,j) != (l,c):
                        self.grille[l][c].remove(self.grille[i][j])
            self.verifier(l,c)
            if self.verbose>1:
                print(f"    END")

        # Methode de recherche : Exclusion (ap 1 iteration)
        if not self.grilleFinie[l][c] and ites:
            if self.verbose>1:
                print(f"[{short_name}]\tDEBUG : Methode de recherche : Exclusion (ap 1 iteration).....", end='')
            for nb in self.grille[l][c]:
                compteur = [0,0,0]
                for k in range(9):
                    if not self.grilleFinie[l][k] and k != c:
                        for n in self.grille[l][k]:
                            compteur[0] += int(n == nb)
                    if not self.grilleFinie[k][c] and k != l:
                        for n in self.grille[k][c]:
                            compteur[1] += int(n == nb)
                for i in lc:
                    for j in cc:
                        if not self.grilleFinie[i][j] and (i,j) != (l,c):
                            for n in self.grille[i][j]:
                                compteur[2] += int(n == nb)
                if compteur[0] == 0 or compteur[1] == 0 or compteur[2] == 0:
                    self.grilleFinie[l][c] = True
                    self.grille[l][c] = nb  
                    for k in range(9):
                        if not self.grilleFinie[l][k] and self.grille[l][c] in self.grille[l][k] and k != c:
                            self.grille[l][k].remove(self.grille[l][c])
                        if not self.grilleFinie[k][c] and self.grille[l][c] in self.grille[k][c] and k != l:
                            self.grille[k][c].remove(self.grille[l][c])
                    for i in lc:
                        for j in cc:
                            if not self.grilleFinie[i][j] and self.grille[l][c] in self.grille[i][j] and (i,j) != (l,c):
                                self.grille[i][j].remove(self.grille[l][c])
                    break
            if self.verbose>1:
                print(f"    END")

        # Methode de recherche : Paires exclusives
        if not self.grilleFinie[l][c] and ites and len(self.grille[l][c]) == 2:
            if self.verbose>1:
                print(f"[{short_name}]\tDEBUG : Methode de recherche : Paires exclusives.....", end="")

            existe = [False,False,False]
            for k in range(9):
                if not self.grilleFinie[l][k] and self.grille[l][k] == self.grille[l][c] and k != c:
                    existe[0] = True
                if not self.grilleFinie[k][c] and self.grille[k][c] == self.grille[l][c] and k != l:
                    existe[1] = True
            for i in lc:
                for j in cc:
                    if not self.grilleFinie[i][j] and self.grille[i][j] == self.grille[l][c] and (i,j) != (l,c):
                        existe[2] = True
            if existe[0]:
                for k in range(9):
                    if not self.grilleFinie[l][k] and self.grille[l][k] != self.grille[l][c]:
                        for n in self.grille[l][k]:
                            if n in self.grille[l][c]:
                                self.grille[l][k].remove(n)
            if existe[1]:
                for k in range(9):
                    if not self.grilleFinie[k][c] and self.grille[k][c] != self.grille[l][c]:
                        for n in self.grille[k][c]:
                            if n in self.grille[l][c]:
                                self.grille[k][c].remove(n)
            if existe[2]:
                for i in lc:
                    for j in cc:
                        if not self.grilleFinie[i][j] and self.grille[i][j] != self.grille[l][c]:
                            for n in self.grille[i][j]:
                                if n in self.grille[l][c]:
                                    self.grille[i][j].remove(n)
            if self.verbose>1:
                print(f"    END")
               
        # Methode de recherche : Triplets exculsifs (hors triplet induit)
        if not self.grilleFinie[l][c] and ites and len(self.grille[l][c]) == 3:
            if self.verbose>1:
                print(f"[{short_name}]\tINFO : Methode de recherche : Triplets exculsifs (hors triplet induit).....", end="")
            existe = [[],[],[]]
            decompo = [[self.grille[l][c][0],self.grille[l][c][1]],[self.grille[l][c][1],self.grille[l][c][2]],[self.grille[l][c][0],self.grille[l][c][2]]]
            for k in range(9):
                if not self.grilleFinie[l][k] and k != c and (self.grille[l][k] == self.grille[l][c] or self.grille[l][k] in decompo):
                    existe[0].append(self.grille[l][k])
                if not self.grilleFinie[k][c] and k != l and (self.grille[k][c] == self.grille[l][c] or self.grille[k][c] in decompo):
                    existe[1].append(self.grille[k][c])
            for i in lc:
                for j in cc:
                    if not self.grilleFinie[i][j] and (i,j) != (l,c) and (self.grille[i][j] == self.grille[l][c] or self.grille[i][j] in decompo):
                        existe[2].append(self.grille[i][j])
            for k in range(3):
                triplet = []
                if len(existe[k]) == 2:
                    for i in [0,1]:
                        for n in existe[k][i]:
                            if n not in triplet:
                                triplet.append(n)
                    if triplet != self.grille[l][c]:
                        existe[k] = False
                else:
                    existe[k] = False
            if existe[0]:
                for k in range(9):
                    if not self.grilleFinie[l][k] and self.grille[l][k] != self.grille[l][c] and self.grille[l][k] not in existe[0]:
                        for n in self.grille[l][k]:
                            if n in self.grille[l][c]:
                                self.grille[l][k].remove(n)
            if existe[1]:
                for k in range(9):
                    if not self.grilleFinie[k][c] and self.grille[k][c] != self.grille[l][c] and self.grille[k][c] not in existe[1]:
                        for n in self.grille[k][c]:
                            if n in self.grille[l][c]:
                                self.grille[k][c].remove(n)
            if existe[2]:
                for i in lc:
                    for j in cc:
                        if not self.grilleFinie[i][j] and self.grille[i][j] != self.grille[l][c] and self.grille[i][j] not in existe[2]:
                            for n in self.grille[i][j]:
                                if n in self.grille[l][c]:
                                    self.grille[i][j].remove(n)
            if self.verbose>1:
                print(f"    END")
           
    def verifier(self, l=0,c=0):
        short_name = "SudokuSolver.verifier()"
        if not l and not c:
            for i in range(9):
                for j in range(9):
                    if type(self.grille[i][j]) is list:
                        if len(self.grille[i][j]) == 1 and self.grille[i][j][0]:
                            self.grilleFinie[i][j] = True
                            self.grille[i][j] = self.grille[i][j][0]
                    else:
                        if self.grille[i][j] != 0:
                            self.grilleFinie[i][j] = True
        else:
            if type(self.grille[l][c]) is list:
                if len(self.grille[l][c]) == 1 and self.grille[l][c][0]:
                    self.grilleFinie[l][c] = True
                    self.grille[l][c] = self.grille[l][c][0]
                   
    def chercher(self, ee=0,ite=0):
        short_name = "SudokuSolver.chercher()"
        iterations = 0
        self.grilleTest = [[0]*9 for n in range(9)]
        self.grilleBack = [[0]*9 for n in range(9)]
        cellBack = [0,0,9,[]]

        if ee and self.verbose>1:
            print(f"[{short_name}]\tDEBUG : {ite} iter"+"s"*(ite!=1))
        
        if self.verbose>1:
            print(f"[{short_name}]\tDEBUG : "*(ee-1)+"|"*(ee!=0)+"_ couche",ee,end=" => ")
        
        while "solution non determinee":
            self.grilleTest = deepcopy(self.grille)
            for i in range(9):
                for j in range(9):
                    self.solutions(i,j,iterations)
            for i in range(9):
                for j in range(9):
                    if self.grille[i][j] == []:
                        return False
            if self.grilleFinie == [[True]*9 for n in range(9)]:
                if self.verbose>0:
                    print(f"[{short_name}]\tINFO : {iterations} iter"+"s"*(iterations!=1))
                    print_sudoku(self.grille)
                return True
            if self.grilleTest == self.grille:
                self.grilleBack = deepcopy(self.grille)
                for i in range(9):
                    for j in range(9):
                        if not self.grilleFinie[i][j] and cellBack[2] > len(self.grille[i][j]):
                            cellBack = [i,j,len(self.grille[i][j]),self.grille[i][j]]
                for n in cellBack[3]:
                    self.grille[cellBack[0]][cellBack[1]] = n
                    if self.chercher(ee+1,iterations):
                        return True
                    else:
                        self.grilleFinie = [[False]*9 for n in range(9)]
                        self.grille = deepcopy(self.grilleBack)
                        self.verifier()
                return False  
            else:
                iterations += 1
            

# ----------------------------------------------------------------------------------
#  %%                      TEST
# ----------------------------------------------------------------------------------
def _test_sudoku_solver(verbose=1):
    short_name = "Test_sudoku_solver_iteratif"
    execution_time = []
    
    for key, grille in tqdm(SUDOKUS.items(), desc=short_name):
        now = datetime.now() # current date and time
        sudo_solver = SudokuSolver(grille=grille, verbose=verbose)
        if verbose>0:
            print_sudoku(sudo_solver.grille)
        sudo_solver.chercher()
        execution_time.append(datetime.now()-now)
        assert sudo_solver.grille == SUDOKUS_ANSWER.get(key, []) or sudo_solver.grille == SUDOKUS_ANSWER.get(key+"b", [])
    # 0:00:00.060347 => 3 sudokus
    # 0:00:00.061117 => 3 sudokus
    # 0:00:00.025226 => 2 sudokus
    print(np.mean(execution_time))

    
# ----------------------------------------------------------------------------------
#                        MAIN
# ----------------------------------------------------------------------------------
# %% main
if __name__ == '__main__':
    short_name = "sudoku_solver_iteratif"
    _test_sudoku_solver()

