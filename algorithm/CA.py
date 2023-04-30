# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:29:46 2023

@author: pozdro
"""
import random
import numpy as np
from algorithm.Cell import Cell
from algorithm.Statistics import Statistics
import sys
class CA:
    def __init__(self, M_rows, N_cols, p_init_C, allC, allD, kD, kC, minK, maxK, num_of_iter, seed = None):
        # size of CA
        self.M_rows = M_rows
        self.N_cols = N_cols
        self.num_of_iter = num_of_iter
        if seed is None:
            random.seed()
            self.seed = random.randint(1, sys.maxsize)
            random.seed(self.seed)
        else:
            random.seed(seed)
            self.seed = seed
            
        # save cells as a list o tuples (num_of_iter, numpy array of Cell instances)
        self.cells = [(0, self.create_CA(p_init_C, allC, allD, kD, kC, minK, maxK))]

        self.statistics = self.calculate_statistics()
        

    def create_CA(self, p_init_C, allC, allD, kD, kC, minK, maxK):
        CA_cells = np.empty((self.M_rows, self.N_cols), dtype=object)
        id_ = 0
        for i in range(self.M_rows):
            for j in range(self.N_cols):
                # Cells on borders have predefined static properties.
                if i == 0 or i == self.M_rows - 1 or j == 0 or j == self.N_cols - 1:
                    CA_cells[i, j] = Cell(_id = id_, x =j , y = i, state = 0, action = 1, strategy = 0)
                else:
                # the rest of cells have randomly assigned states and strategies
                    state = self.init_cell_state( p_init_C)
                    strategy, k = self.init_cell_strategy(allC, allD, kD, kC, minK, maxK)
                    CA_cells[i, j] = Cell(_id = id_, x = j, y = i, strategy = strategy, k = k, state = state)
                id_ += 1
        return CA_cells
    
    # initially cell states are assigned randomly with p_init_C probability.
    def init_cell_state(self, p_init_C):
            x = random.random()
            if x <= p_init_C:
                state = 1
            else:
                state = 0
            return state
   
    # initially cell strategies are assigned randomly with user-defined probabilities                 
    def init_cell_strategy(self, allC, allD, kD, kC, minK, maxK):
        b1 = allC
        b2 = allD + b1
        b3 = kD + b2
        b4 = kC + b3
        x = random.random()
        if x <= b1:
            strategy = 1
            k = -1
        elif x <= b2:
            strategy = 0
            k = -1
        elif x <= b3:
            strategy = 2
            y = random.randint(minK, maxK)
            k = y
        elif x <= b4:
            strategy = 3
            y = random.randint(minK, maxK)
            k = y
        else: 
            strategy = 4
            y = random.randint(minK, maxK)
            k = y
        return strategy, k


    # def evolution(self):
    #     cells_temp = np.empty((self.M_rows, self.N_cols), dtype=object)
    #     for k in range(0, self.num_of_iter):
    #         iter1, cells = self.cells[k]
    #         for i in range(1, self.M_rows - 1):
    #             for j in range(1, self.N_cols - 1):
    #                 cells[i, j].action = self.decide_action(i, j, cells)
    #







    def decide_action(self, i, j, cells):
        return self.is_C_correct(cells, i, j) or self.is_D_correct(cells, i, j)

    def calculate_statistics(self):

        statistics = []
        for k, cells in self.cells:
            num_of_cells = 0
            num_of_C = 0
            num_of_C_corr = 0
            num_of_allC = 0
            num_of_allD = 0
            num_of_kD = 0
            num_of_kC = 0
            num_of_kDC = 0
            num_of_strat_change = 0
            num_of_0D = num_of_1D = num_of_2D = num_of_3D = num_of_4D = num_of_5D = num_of_6D = num_of_7D = num_of_8D = 0
            num_of_0C = num_of_1C = num_of_2C = num_of_3C = num_of_4C = num_of_5C = num_of_6C = num_of_7C = num_of_8C = 0
            num_of_0DC = num_of_1DC = num_of_2DC = num_of_3DC = num_of_4DC = num_of_5DC = num_of_6DC = num_of_7DC = num_of_8DC = 0

            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    num_of_cells += 1
                    if cells[i, j].state == 1:
                        num_of_C += 1
                        if self.is_C_correct(cells, i, j):
                            num_of_C_corr += 1

                    # all D
                    if cells[i, j].strategy == 0:
                        num_of_allD += 1
                    # all C
                    elif cells[i, j].strategy == 1:
                        num_of_allC += 1
                    # kD
                    elif cells[i, j].strategy == 2:
                        num_of_kD += 1
                        if cells[i, j].k == 0:
                            num_of_0D += 1
                        elif cells[i, j].k == 1:
                            num_of_1D += 1
                        elif cells[i, j].k == 2:
                            num_of_2D += 1
                        elif cells[i, j].k == 3:
                            num_of_3D += 1
                        elif cells[i, j].k == 4:
                            num_of_4D += 1
                        elif cells[i, j].k == 5:
                            num_of_5D += 1
                        elif cells[i, j].k == 6:
                            num_of_6D += 1
                        elif cells[i, j].k == 7:
                            num_of_7D += 1
                        elif cells[i, j].k == 8:
                            num_of_8D += 1

                    # kC
                    elif cells[i, j].strategy == 3:
                        num_of_kC += 1
                        if cells[i, j].k == 0:
                            num_of_0C += 1
                        elif cells[i, j].k == 1:
                            num_of_1C += 1
                        elif cells[i, j].k == 2:
                            num_of_2C += 1
                        elif cells[i, j].k == 3:
                            num_of_3C += 1
                        elif cells[i, j].k == 4:
                            num_of_4C += 1
                        elif cells[i, j].k == 5:
                            num_of_5C += 1
                        elif cells[i, j].k == 6:
                            num_of_6C += 1
                        elif cells[i, j].k == 7:
                            num_of_7C += 1
                        elif cells[i, j].k == 8:
                            num_of_8C += 1

                    # kDC
                    elif cells[i, j].strategy == 4:
                        num_of_kDC += 1
                        if cells[i, j].k == 0:
                            num_of_0DC += 1
                        elif cells[i, j].k == 1:
                            num_of_1DC += 1
                        elif cells[i, j].k == 2:
                            num_of_2DC += 1
                        elif cells[i, j].k == 3:
                            num_of_3DC += 1
                        elif cells[i, j].k == 4:
                            num_of_4DC += 1
                        elif cells[i, j].k == 5:
                            num_of_5DC += 1
                        elif cells[i, j].k == 6:
                            num_of_6DC += 1
                        elif cells[i, j].k == 7:
                            num_of_7DC += 1
                        elif cells[i, j].k == 8:
                            num_of_8DC += 1

            # calculate the stats
            f_C = num_of_C / num_of_cells
            f_C_corr = num_of_C_corr / num_of_cells
            av_sum = 0
            f_allC = num_of_allC / num_of_cells
            f_allD = num_of_allD / num_of_cells
            f_kD = num_of_kD / num_of_cells
            f_kC = num_of_kC / num_of_cells
            f_kDC = num_of_kDC / num_of_cells
            f_strat_ch = num_of_strat_change / num_of_cells
            f_0D = num_of_0D / num_of_kD
            f_1D = num_of_1D / num_of_kD
            f_2D = num_of_2D / num_of_kD
            f_3D = num_of_3D / num_of_kD
            f_4D = num_of_4D / num_of_kD
            f_5D = num_of_5D / num_of_kD
            f_6D = num_of_6D / num_of_kD
            f_7D = num_of_7D / num_of_kD
            f_8D = num_of_8D / num_of_kD

            f_0C = num_of_0C / num_of_kC
            f_1C = num_of_1C / num_of_kC
            f_2C = num_of_2C / num_of_kC
            f_3C = num_of_3C / num_of_kC
            f_4C = num_of_4C / num_of_kC
            f_5C = num_of_5C / num_of_kC
            f_6C = num_of_6C / num_of_kC
            f_7C = num_of_7C / num_of_kC
            f_8C = num_of_8C / num_of_kC

            f_0DC = num_of_0DC / num_of_kDC
            f_1DC = num_of_1DC / num_of_kDC
            f_2DC = num_of_2DC / num_of_kDC
            f_3DC = num_of_3DC / num_of_kDC
            f_4DC = num_of_4DC / num_of_kDC
            f_5DC = num_of_5DC / num_of_kDC
            f_6DC = num_of_6DC / num_of_kDC
            f_7DC = num_of_7DC / num_of_kDC
            f_8DC = num_of_8DC / num_of_kDC

            # save stats as list of Statistics class instances
            statistics.append((Statistics(k, f_C, f_C_corr, av_sum, f_allC, f_allD, f_kD, f_kC,
                     f_kDC, f_strat_ch, f_0D, f_1D, f_2D, f_3D, f_4D, f_5D, f_6D,
                     f_7D, f_8D, f_0C, f_1C, f_2C, f_3C, f_4C, f_5C, f_6C, f_7C, f_8C,
                     f_0DC, f_1DC, f_2DC, f_3DC, f_4DC, f_5DC, f_6DC, f_7DC, f_8DC)))
        return statistics

    def is_C_correct(self, cells, i, j):
        if cells[i, j].state == 1:
            if cells[i - 1, j - 1].state == 0 and cells[i - 1, j].state == 0 and cells[i - 1, j + 1].state == 0:
                if cells[i, j - 1].state == 0 and cells[i, j + 1].state == 0:
                    if cells[i + 1, j - 1].state == 0 and cells[i + 1, j].state == 0 and cells[i + 1, j + 1].state == 0:
                        return True
        return False
    def is_D_correct(self, cells, i, j):
        if cells[i, j].state == 0:
            # neighbours with 1s in corners
            if cells[i - 1, j - 1].state == 1 and cells[i - 1, j].state == 0 and cells[i - 1, j + 1].state == 1:
                if cells[i, j - 1]. state == 0 and cells[i, j + 1].state == 0:
                    if cells[i + 1, j - 1].state == 1 and cells[i + 1, j].state == 0 and cells[i + 1, j + 1].state == 1:
                        return True
            # neighbours with 1s up and down
            elif cells[i - 1, j - 1].state == 0 and cells[i - 1, j].state == 1 and cells[i - 1, j + 1].state == 0:
                if cells[i, j - 1]. state == 0 and cells[i, j + 1].state == 0:
                    if cells[i + 1, j - 1].state == 0 and cells[i + 1, j].state == 1 and cells[i + 1, j + 1].state == 0:
                        return True
            # neighbours with 1s left and right
            elif cells[i - 1, j - 1].state == 0 and cells[i - 1, j].state == 0 and cells[i - 1, j + 1].state == 0:
                if cells[i, j - 1]. state == 1 and cells[i, j + 1].state == 1:
                    if cells[i + 1, j - 1].state == 0 and cells[i + 1, j].state == 0 and cells[i + 1, j + 1].state == 0:
                        return True
        return False