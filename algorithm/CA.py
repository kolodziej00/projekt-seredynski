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
import copy




class CA:
    def __init__(self, M_rows, N_cols, p_init_C, allC, allD, kD, kC, minK, maxK, num_of_iter,
                 payoff_C_C, payoff_C_D, payoff_D_C, payoff_D_D, is_sharing, synch_prob,
                 is_tournament, seed = None):
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

        # payoff values from GUI
        self.payoff_C_C = payoff_C_C
        self.payoff_C_D = payoff_C_D
        self.payoff_D_C = payoff_D_C
        self.payoff_D_D = payoff_D_D
        self.avg_payoff = []

        # sharing of payoffs
        self.is_sharing = is_sharing

        # competition type, if true - tournament competition else roulette competition
        self.is_tournament = is_tournament

        # probability that cell will change strategy in each iteration
        self.synch_prob = synch_prob

        # save cells as a list o tuples (num_of_iter, numpy array of Cell instances)
        self.cells = [(0, self.create_CA(p_init_C, allC, allD, kD, kC, minK, maxK))]
        self.evolution()
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


    def evolution(self):

        for k in range(0, self.num_of_iter - 1):
            sum_payoff_temp = 0
            iter1, cells = self.cells[k]

            # decide action and check if cell is in group_of_1s or group_of_0s
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    cells[i, j].action = self.decide_action(cells, i, j)
                    cells[i, j].group_of_1s  = self.is_group_of_1s(cells, i, j)
                    if not cells[i, j].group_of_1s:
                        cells[i, j].group_of_0s = self.is_group_of_0s(cells, i, j)
                    # decide whether cell will be changing strategy in this iteration
                    self.is_cell_changing_start(cells[i, j])


            # calculate payoffs
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    self.calculate_payoff(cells, i, j)
                    sum_payoff_temp += cells[i, j].sum_payoff
            self.avg_payoff.append((k, sum_payoff_temp / cells.size))
            cells_temp = copy.deepcopy(cells)

            # competition - for now only tournament comp.
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    if cells_temp[i, j].change_strategy:
                        self.tournament_competition(cells, cells_temp, i, j)





            self.cells.append((k + 1, cells_temp))

        # not ideal but works...
        self.avg_payoff.append(self.avg_payoff[self.num_of_iter - 2])
    def tournament_competition(self, cells, cells_temp, i, j):
        max_payoff = (i, j, cells[i, j].sum_payoff)
        for k in range(i - 1, i + 2):
            for n in range(j - 1, j + 2):
                if k == i and n == j:
                    continue
                if max_payoff[2] < cells[k, n].sum_payoff:
                    max_payoff = (k, n, cells[k, n].sum_payoff)
        k, n, payoff = max_payoff
        if k != i or n != j:
            cells_temp[i, j].strategy = cells[k, n].strategy
            cells_temp[i, j].k = cells[k, n].k

    def calculate_payoff(self, cells, i , j):
        # action is D
        m = 0
        if cells[i, j].action == 0:
            # if cell is in group_of_1s or group_of_0s then all cells in neighbourhood have action = D (= 0)
            if cells[i, j].group_of_1s or cells[i, j].group_of_0s:
                for k in range(8):
                    cells[i, j].payoffs[k] = self.payoff_D_D
                    cells[i, j].sum_payoff += self.payoff_D_D
            # for loop over cell's neighbours
            for k in range(i - 1,  i + 2):
                for n in range(j - 1, j + 2):
                    if k == i and j == n:
                        continue
                    if cells[k, n].action == 1:
                        cells[i, j].payoffs[m] = self.payoff_D_C
                        cells[i, j].sum_payoff += self.payoff_D_C
                    elif cells[k, n].action == 0:
                        cells[i, j].payoffs[m] = self.payoff_D_D
                        cells[i, j].sum_payoff += self.payoff_D_D

                    m += 1
        elif cells[i, j].action == 1:
            # if cell's action is C then cell can't be in group_of_1s or group_of_0s
            for k in range(i - 1,  i + 2):
                for n in range(j - 1, j + 2):
                    if k == i == j == n:
                        continue
                    if cells[k, n].action == 1:
                        cells[i, j].payoffs[m] = self.payoff_C_C
                        cells[i, j].sum_payoff += self.payoff_C_C
                    elif cells[k, n].action == 0:
                        cells[i, j].payoffs[m] = self.payoff_C_D
                        cells[i, j].sum_payoff += self.payoff_C_D
        cells[i, j].avg_payoff = cells[i, j].sum_payoff / 8



    def is_group_of_0s(self, cells, i, j):
        if cells[i, j].state == 0:
            if cells[i - 1, j - 1].state == 0 and cells[i - 1, j].state == 0 and cells[i - 1, j + 1].state == 0:
                if cells[i, j - 1].state == 0 and cells[i, j + 1].state == 0:
                    if cells[i + 1, j - 1].state == 0 and cells[i + 1, j].state == 0 and cells[i + 1, j + 1].state == 0:
                        return True
        return False

    def is_group_of_1s(self, cells, i, j):
        if cells[i, j].state == 1:
            if cells[i - 1, j - 1].state == 1 and cells[i - 1, j].state == 1 and cells[i - 1, j + 1].state == 1:
                if cells[i, j - 1].state == 1 and cells[i, j + 1].state == 1:
                    if cells[i + 1, j - 1].state == 1 and cells[i + 1, j].state == 1 and cells[i + 1, j + 1].state == 1:
                        return True
        return False

    def is_cell_changing_start(self, cell):
        if self.synch_prob == 1:
            cell.change_strategy = True
        else:
            x = random.random()
            if x <= self.synch_prob:
                cell.change_strategy = True
            else:
                cell.change_strategy = False

    def decide_action(self, cells, i, j):
        if self.is_C_correct(cells, i, j):
            return 1
        elif self.is_D_correct(cells, i, j):
            return 1
        else:
            return 0

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
                if cells[i, j - 1].state == 0 and cells[i, j + 1].state == 0:
                    if cells[i + 1, j - 1].state == 1 and cells[i + 1, j].state == 0 and cells[i + 1, j + 1].state == 1:
                        return True
            # neighbours with 1s up and down
            elif cells[i - 1, j - 1].state == 0 and cells[i - 1, j].state == 1 and cells[i - 1, j + 1].state == 0:
                if cells[i, j - 1].state == 0 and cells[i, j + 1].state == 0:
                    if cells[i + 1, j - 1].state == 0 and cells[i + 1, j].state == 1 and cells[i + 1, j + 1].state == 0:
                        return True
            # neighbours with 1s left and right
            elif cells[i - 1, j - 1].state == 0 and cells[i - 1, j].state == 0 and cells[i - 1, j + 1].state == 0:
                if cells[i, j - 1].state == 1 and cells[i, j + 1].state == 1:
                    if cells[i + 1, j - 1].state == 0 and cells[i + 1, j].state == 0 and cells[i + 1, j + 1].state == 0:
                        return True
        return False

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

                    # this is wrong - even if change_strategy it doesn't mean that cell changed strat...
                    if cells[i, j].change_strategy == True:
                        num_of_strat_change += 1

            # calculate the stats
            f_C = num_of_C / num_of_cells
            f_C_corr = num_of_C_corr / num_of_cells
            iter1, av_sum = self.avg_payoff[k]
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

