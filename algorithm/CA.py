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
                 is_tournament, p_state_mut, p_strat_mut, p_0_neigh_mut, p_1_neigh_mut, is_debug, is_test1, is_test2,
                 f, optimal_num1s, seed=None):
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

        self.optimal_num_1s = optimal_num1s

        # payoff values from GUI
        self.payoff_C_C = payoff_C_C
        self.payoff_C_D = payoff_C_D
        self.payoff_D_C = payoff_D_C
        self.payoff_D_D = payoff_D_D
        self.avg_payoff = []

        # sharing of payoffs
        self.is_sharing = is_sharing

        # debug options
        self.is_debug = is_debug
        self.is_test1 = is_test1
        self.is_test2 = is_test2
        self.f = f

        # competition type, if true - tournament competition, else roulette competition
        self.is_tournament = is_tournament

        # probability that cell will change strategy in each iteration
        self.synch_prob = synch_prob

        # mutations probabilities
        self.p_state_mut = p_state_mut
        self.p_strat_mut = p_strat_mut
        self.p_neigh_0_mut = p_0_neigh_mut
        self.p_neigh_1_mut = p_1_neigh_mut

        # min K, max K
        self.minK = minK
        self.maxK = maxK

        # (iter, f_strat_ch, f_strat_ch_final)
        self.misc_stats = [(0, 0, 0)]
        # save cells as a list o tuples (num_of_iter, numpy array of Cell instances)
        if not self.is_debug:
            self.cells = [(0, self.create_CA(p_init_C, allC, allD, kD, kC, minK, maxK))]
        else:
            self.cells = [(0, self.create_CA_debug())]
        self.evolution()
        self.statistics = self.calculate_statistics()

    def create_CA_debug(self):
        # read file to list of strings
        f1 = open("CA_states_deb.txt", "r")
        f2 = open("CA_strat_deb.txt", "r")
        ca_states_lines = f1.readlines()
        ca_strat_lines = f2.readlines()

        cells = np.empty((self.M_rows, self.N_cols), dtype=object)
        id_ = 1
        for i in range(self.M_rows):
            if 1 <= i <= self.M_rows - 2:
                ca_states_lines_separated = ca_states_lines[i - 1].split(" ")
                ca_strat_lines_separated = ca_strat_lines[i - 1].split(" ")
            for j in range(self.N_cols):
                # Cells on borders have predefined static properties.
                if i == 0 or i == self.M_rows - 1 or j == 0 or j == self.N_cols - 1:
                    cells[i, j] = Cell(_id=0, x=j, y=i, state=0, action=1, strategy=0)
                    cells[i, j].avg_payoff = 1.0
                    continue
                strategy = int(ca_strat_lines_separated[j - 1][0])
                if strategy == 1 or strategy == 0:
                    k = 0
                else:
                    k = int(ca_strat_lines_separated[j - 1][1])
                cells[i, j] = Cell(_id=id_, x=j, y=i, state=int(ca_states_lines_separated[j - 1]),
                                   strategy=strategy, k=k)
                id_ += 1
        if self.is_debug:
            # print states
            self.f.write("iter=0\nCA_states:\n")
            for i in range(self.M_rows):
                for j in range(self.N_cols):
                    self.f.write("{0:<2}".format(cells[i, j].state))
                self.f.write("\n")

            # print strategies
            self.f.write("\nCA_strat:\n")
            for i in range(self.M_rows):
                for j in range(self.N_cols):
                    if cells[i, j].strategy == 1 or cells[i, j].strategy == 0:
                        self.f.write("{0:<4}".format(cells[i, j].strategy))
                    else:
                        self.f.write("{0:1}{1:<3}".format(cells[i, j].strategy, cells[i, j].k))
                self.f.write("\n")

            # print kD strat
            self.f.write("\nCA_kD_strat:\n")
            for i in range(self.M_rows):
                for j in range(self.N_cols):
                    if cells[i, j].strategy == 2:
                        self.f.write("{0:1}{1:<3}".format(cells[i, j].strategy, cells[i, j].k))
                    else:
                        self.f.write("{0:<4}".format(-1))
                self.f.write("\n")

            # print kC strat
            self.f.write("\nCA_kC_strat:\n")
            for i in range(self.M_rows):
                for j in range(self.N_cols):
                    if cells[i, j].strategy == 3:
                        self.f.write("{0:1}{1:<3}".format(cells[i, j].strategy, cells[i, j].k))
                    else:
                        self.f.write("{0:<4}".format(-1))
                self.f.write("\n")

            # print kDC strat
            self.f.write("\nCA_kDC_strat:\n")
            for i in range(self.M_rows):
                for j in range(self.N_cols):
                    if cells[i, j].strategy == 4:
                        self.f.write("{0:1}{1:<3}".format(cells[i, j].strategy, cells[i, j].k))
                    else:
                        self.f.write("{0:<4}".format(-1))
                self.f.write("\n")

            # print agent_glob_id
            self.f.write("\nAgent_glob_ID:\n")
            for i in range(self.M_rows):
                for j in range(self.N_cols):
                    self.f.write("{0:<5}".format(cells[i, j].id))
                self.f.write("\n")

            # print agent_i_j_id
            self.f.write("\nAgent_i_j_ID:\n")
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    self.f.write("{0:<5}{1:<5}".format(cells[i, j].x, cells[i, j].y))
                    self.f.write("\n")

            # print agent neighbours
            self.f.write("\nAgent_neighbors:\n")
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    self.f.write("{0:<5}{1:<5}{2:<5}{3:<5}".format(cells[i - 1, j].id, cells[i - 1, j + 1].id,
                                                               cells[i, j + 1].id, cells[i + 1, j + 1].id))
                    self.f.write("{0:<5}{1:<5}{2:<5}{3:<5}".format(cells[i + 1, j].id, cells[i + 1, j - 1].id,
                                                               cells[i, j - 1].id, cells[i - 1, j - 1].id))
                    self.f.write("\n")

            self.f.write("\nkD:\n")
            self.f.write("1 0 0 0 0 0 0 0 0\n1 1 0 0 0 0 0 0 0\n1 1 1 0 0 0 0 0 0\n1 1 1 1 0 0 0 0 0\n")
            self.f.write("1 1 1 1 1 0 0 0 0\n1 1 1 1 1 1 0 0 0\n1 1 1 1 1 1 1 0 0\n1 1 1 1 1 1 1 1 0\n")
            self.f.write("1 1 1 1 1 1 1 1 1\n")

            self.f.write("\nkC:\n")
            self.f.write("0 0 0 0 0 0 0 0 1\n0 0 0 0 0 0 0 1 1\n0 0 0 0 0 0 1 1 1\n0 0 0 0 0 1 1 1 1\n")
            self.f.write("0 0 0 0 1 1 1 1 1\n0 0 0 1 1 1 1 1 1\n0 0 1 1 1 1 1 1 1\n0 1 1 1 1 1 1 1 1\n")
            self.f.write("1 1 1 1 1 1 1 1 1\n")

            self.f.write("\nkDC:\n")
            self.f.write("0 1 1 1 1 1 1 1 1\n0 0 1 1 1 1 1 1 1\n0 0 0 1 1 1 1 1 1\n0 0 0 0 1 1 1 1 1\n")
            self.f.write("0 0 0 0 0 1 1 1 1\n0 0 0 0 0 0 1 1 1\n0 0 0 0 0 0 0 1 1\n0 0 0 0 0 0 0 0 1\n")
            self.f.write("0 0 0 0 0 0 0 0 0\n")




        return cells

    def create_CA(self, p_init_C, allC, allD, kD, kC, minK, maxK):
        CA_cells = np.empty((self.M_rows, self.N_cols), dtype=object)
        id_ = 1
        for i in range(self.M_rows):
            for j in range(self.N_cols):
                # Cells on borders have predefined static properties.
                if i == 0 or i == self.M_rows - 1 or j == 0 or j == self.N_cols - 1:
                    CA_cells[i, j] = Cell(_id=0, x=j, y=i, state=0, action=1, strategy=0)
                    CA_cells[i, j].avg_payoff = 1.0
                    continue
                else:
                    # the rest of cells have randomly assigned states and strategies
                    state = self.init_cell_state(p_init_C)
                    strategy, k = self.init_cell_strategy(allC, allD, kD, kC, minK, maxK)
                    CA_cells[i, j] = Cell(_id=id_, x=j, y=i, strategy=strategy, k=k, state=state)
                id_ += 1
        for i in range(1, self.M_rows - 1):
            for j in range(1, self.N_cols - 1):
                CA_cells[i, j].group_of_1s = self.is_group_of_1s(CA_cells, i, j)
                if CA_cells[i, j].group_of_1s:
                    CA_cells[i, j].group_of_0s = False
                    continue
                else:
                    CA_cells[i, j].group_of_0s = self.is_group_of_0s(CA_cells, i, j)

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
            change_strat_count = 0
            change_strat_count_final = 0
            if self.is_debug and self.is_test1:
                if k != 0:
                  self.f.write("\niter= " + str(k))
                self.f.write("\nCALCULATE C*/D*\n")
            # decide action
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    cells[i, j].action = self.decide_action(cells, i, j)
                    cells[i, j].group_of_1s = self.is_group_of_1s(cells, i, j)
                    if not cells[i, j].group_of_1s:
                        cells[i, j].group_of_0s = self.is_group_of_0s(cells, i, j)
                    if self.is_debug and self.is_test1:
                        self.f.write("\nid={0:3}\n".format(cells[i, j].id))
                        self.f.write("My_neighb_states:\n")
                        self.f.write("{0:2}{1:2}{2:2}{3:2}".format(cells[i - 1, j].state, cells[i - 1, j + 1].state,
                                                                   cells[i, j + 1].state, cells[i + 1, j + 1].state))
                        self.f.write("{0:2}{1:2}{2:2}{3:2}\n".format(cells[i + 1, j].state, cells[i + 1, j - 1].state,
                                                                   cells[i, j - 1].state, cells[i - 1, j - 1].state))
                    # decide whether cell will be changing strategy in this iteration with synch_prob probability
                    self.is_cell_changing_strategy(cells[i, j])
            if self.is_debug and self.is_test1:
                self.f.write("\nCA_actions:\n")
                for i in range(self.M_rows):
                    for j in range(self.N_cols):
                        self.f.write("{0:<3}".format(cells[i, j].action))
                    self.f.write("\n")
                self.f.write("\nGroup_8_0s:\n")
                for i in range(1, self.M_rows - 1):
                    for j in range(1, self.N_cols - 1):
                        if cells[i, j].group_of_0s:
                            self.f.write("{0:<3}".format(1))
                        else:
                            self.f.write("{0:<3}".format(0))
                    self.f.write("\n")

                self.f.write("\nGroup_8_1s:\n")
                for i in range(1, self.M_rows - 1):
                    for j in range(1, self.N_cols - 1):
                        if cells[i, j].group_of_1s:
                            self.f.write("{0:<3}".format(1))
                        else:
                            self.f.write("{0:<3}".format(0))
                    self.f.write("\n")

            # calculate payoffs
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    self.calculate_payoff(cells, i, j)
                    sum_payoff_temp += cells[i, j].avg_payoff

            avg_payoff_temp = sum_payoff_temp / ((self.M_rows - 2) * (self.N_cols - 2))


            if self.is_debug and self.is_test1:
                # print payoffs
                self.f.write("\nPayoffs:\n")
                for i in range(1, self.M_rows - 1):
                    for j in range(1, self.N_cols - 1):
                        self.f.write("{0:5.1f}{1:5.1f}{2:5.1f}{3:5.1f}".format(cells[i, j].payoffs[1], cells[i, j].payoffs[2],
                                                                   cells[i, j].payoffs[4], cells[i, j].payoffs[7]))
                        self.f.write("{0:5.1f}{1:5.1f}{2:5.1f}{3:5.1f}\n".format(cells[i, j].payoffs[6], cells[i, j].payoffs[5],
                                                                     cells[i, j].payoffs[3], cells[i, j].payoffs[0]))
                if not self.is_sharing:
                    self.f.write("\nCumul_payoffs:\n")
                    for i in range(1, self.M_rows - 1):
                        for j in range(1, self.N_cols - 1):
                            self.f.write("{0:<5.1f}\n".format(cells[i, j].sum_payoff))

                    self.f.write("\nCumul_avg:\n")
                    for i in range(1, self.M_rows - 1):
                        for j in range(1, self.N_cols - 1):
                            self.f.write("{0:<5.4f}\n".format(cells[i, j].avg_payoff))
                    self.f.write("\nav_pay = {0:<5.4f}\n".format(avg_payoff_temp))



            # copy cells to new array to change strategies and states
            cells_temp = copy.deepcopy(cells)

            # redistribute payoffs
            if self.is_sharing:
                sum_payoff_temp = 0
                for i in range(1, self.M_rows - 1):
                    for j in range(1, self.N_cols - 1):
                        self.redistribute_payoff(cells, cells_temp, i, j)
                        sum_payoff_temp += cells[i, j].avg_payoff

            self.avg_payoff.append((k, sum_payoff_temp / ((self.M_rows - 2) * (self.N_cols - 2))))

            if self.is_debug and self.is_test1 and self.is_sharing:
                # print payoffs
                self.f.write("\nPayoffs after redistribution:\n")
                for i in range(1, self.M_rows - 1):
                    for j in range(1, self.N_cols - 1):
                        self.f.write("{0:5.1f}{1:5.1f}{2:5.1f}{3:5.1f}".format(cells[i, j].payoffs[1], cells[i, j].payoffs[2],
                                                                   cells[i, j].payoffs[4], cells[i, j].payoffs[7]))
                        self.f.write("{0:5.1f}{1:5.1f}{2:5.1f}{3:5.1f}\n".format(cells[i, j].payoffs[6], cells[i, j].payoffs[5],
                                                                     cells[i, j].payoffs[3], cells[i, j].payoffs[0]))

                self.f.write("\nCumul_payoffs:\n")
                for i in range(1, self.M_rows - 1):
                    for j in range(1, self.N_cols - 1):
                        self.f.write("{0:<5.1f}\n".format(cells[i, j].sum_payoff))

                self.f.write("\nCumul_avg:\n")
                for i in range(1, self.M_rows - 1):
                    for j in range(1, self.N_cols - 1):
                        self.f.write("{0:<5.4f}\n".format(cells[i, j].avg_payoff))
                _, avg_payoff = self.avg_payoff[k]
                self.f.write("\nav_pay = {0:<5.4f}\n".format(avg_payoff))

            # cells change strategy for competition winning cell's strategy with sync_prob probability
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    if cells_temp[i, j].change_strategy:
                        if self.is_tournament:
                            if self.tournament_competition(cells, cells_temp, i, j):
                                change_strat_count += 1
                        else:
                            if self.roulette_competition(cells, cells_temp, i, j):
                                change_strat_count += 1

                    if cells_temp[i, j].strategy != cells[i, j].strategy:
                        change_strat_count_final += 1
                    else:
                        if (cells[i, j].strategy == 2 or cells[i, j].strategy == 3 or cells[i, j].strategy == 4) and \
                                cells[i, j].k != cells_temp[i, j].k:
                            change_strat_count_final += 1
                    # strategy mutation with p_strat_mut probability
                    if self.p_strat_mut != 0:
                        x = random.random()
                        if x <= self.p_strat_mut:
                            self.mutate_strat(cells_temp[i, j])

            # update cell states depending on strategy
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):

                    self.update_cell_states(cells, cells_temp, i, j)

                    # resetting group_of_1s and 0s to avoid false state changes in next step
                    cells_temp[i, j].group_of_1s = False
                    cells_temp[i, j].group_of_0s = False

                    # cell state mutation with p_state_mut probability
                    if self.p_state_mut != 0:
                        x = random.random()
                        if x <= self.p_state_mut:
                            self.mutate_state(cells_temp[i, j])

            if self.is_debug and self.is_test2:
                # winner_agent
                self.f.write("\nWinner agent:\n")
                for i in range(1, self.M_rows - 1):
                    for j in range(1, self.N_cols - 1):
                        self.f.write("{0:<4}\n".format(cells[i, j].winner_agent))

                # CA start
                self.f.write("\nCA_strat:\n")
                for i in range(self.M_rows):
                    for j in range(self.N_cols):
                        if cells_temp[i, j].strategy == 1 or cells_temp[i, j].strategy == 0:
                            self.f.write("{0:<4}".format(cells_temp[i, j].strategy))
                        else:
                            self.f.write("{0:1}{1:<3}".format(cells_temp[i, j].strategy, cells_temp[i, j].k))
                    self.f.write("\n")

                # print kD strat
                self.f.write("\nCA_kD_strat:\n")
                for i in range(self.M_rows):
                    for j in range(self.N_cols):
                        if cells_temp[i, j].strategy == 2:
                            self.f.write("{0:1}{1:<3}".format(cells_temp[i, j].strategy, cells_temp[i, j].k))
                        else:
                            self.f.write("{0:<4}".format(-1))
                    self.f.write("\n")

                # print kC strat
                self.f.write("\nCA_kC_strat:\n")
                for i in range(self.M_rows):
                    for j in range(self.N_cols):
                        if cells_temp[i, j].strategy == 3:
                            self.f.write("{0:1}{1:<3}".format(cells_temp[i, j].strategy, cells_temp[i, j].k))
                        else:
                            self.f.write("{0:<4}".format(-1))
                    self.f.write("\n")

                # print kDC strat
                self.f.write("\nCA_kDC_strat:\n")
                for i in range(self.M_rows):
                    for j in range(self.N_cols):
                        if cells_temp[i, j].strategy == 4:
                            self.f.write("{0:1}{1:<3}".format(cells_temp[i, j].strategy, cells_temp[i, j].k))
                        else:
                            self.f.write("{0:<4}".format(-1))
                    self.f.write("\n")
                f_strat_ch = change_strat_count / ((self.M_rows - 2) * (self.N_cols - 2))
                f_strat_ch_final = change_strat_count_final / ((self.M_rows - 2) * (self.N_cols - 2))
                self.f.write("\nf_start_ch = {0:4.3f}\n".format(f_strat_ch))
                self.f.write("\nf_start_ch_fin = {0:4.3f}\n".format(f_strat_ch_final))

                # print states
                self.f.write("\nCA_states:\n")
                for i in range(self.M_rows):
                    for j in range(self.N_cols):
                        self.f.write("{0:<2}".format(cells_temp[i, j].state))
                    self.f.write("\n")

            # mutation when cell is in group od 1s or group of 0s
            # (shouldn't it be done earlier?)
            for i in range(1, self.M_rows - 1):
                for j in range(1, self.N_cols - 1):
                    cells_temp[i, j].group_of_1s = self.is_group_of_1s(cells_temp, i, j)
                    if not cells_temp[i, j].group_of_1s:
                        cells_temp[i, j].group_of_0s = self.is_group_of_0s(cells_temp, i, j)
                    if cells_temp[i, j].group_of_0s:
                        x = random.random()
                        if x <= self.p_neigh_0_mut:
                            cells_temp[i, j].state = 1
                    elif cells_temp[i, j].group_of_1s:
                        x = random.random()
                        if x <= self.p_neigh_1_mut:
                            cells_temp[i, j].state = 0
            self.misc_stats.append((k + 1, change_strat_count, change_strat_count_final))
            self.cells.append((k + 1, cells_temp))

        # not ideal but works...
        self.avg_payoff.append(self.avg_payoff[self.num_of_iter - 2])

    # mutation of cell state by negating current state
    def mutate_state(self, cell):
        if cell.state == 0:
            cell.state = 1
        else:
            cell.state = 0

    # mutation of strategy - for now simple random choice
    def mutate_strat(self, cell):
        x = random.randint(0, 4)
        if cell.strategy == 0:
            cell.strategy = 1
        elif cell.strategy == 1:
            cell.strategy = 0
        else:
            if self.minK == self.maxK:
                return
            if cell.k == self.minK:
                cell.k += 1
            elif cell.k == self.maxK:
                cell.k -= 1
            else:
                cell.k = random.choice((cell.k - 1, cell.k + 1))

    def update_cell_states(self, cells, cells_temp, i, j):
        # all D
        if cells_temp[i, j].strategy == 0:
            cells_temp[i, j].state = 0
            return
        # all C
        elif cells_temp[i, j].strategy == 1:
            cells_temp[i, j].state = 1
            return
        # kC and kD
        elif cells_temp[i, j].strategy == 3:
            # calculate K for neighbourhood in previous iteration
            k = self.calculate_k_neighbours(cells, i, j)
            if k <= cells_temp[i, j].k:
                cells_temp[i, j].state = 1
            else:
                cells_temp[i, j].state = 0
        elif cells_temp[i, j].strategy == 2:
            k = self.calculate_k_neighbours(cells, i, j)
            if 8 - k <= cells_temp[i, j].k:
                cells_temp[i, j].state = 1
            else:
                cells_temp[i, j].state = 0
        elif cells_temp[i, j].strategy == 4:
            k = self.calculate_k_neighbours(cells, i, j)
            if 8 - k <= cells_temp[i, j].k:
                cells_temp[i, j].state = 0
            else:
                cells_temp[i, j].state = 1

    # calculate how many neighbours defect/cooperate
    def calculate_k_neighbours(self, cells, i, j):
        # count of neighbours with state==1
        k_1_count = 0
        # loop over neighbourhood
        for n in range(i - 1, i + 2):
            for m in range(j - 1, j + 2):
                if n == i and m == j:
                    continue
                if cells[n, m].state == 1:
                    k_1_count += 1

        return k_1_count

    # tournament competition - wins neighbour with the highest payoff
    def tournament_competition(self, cells, cells_temp, i, j):
        cells[i, j].winner_agent = -1
        max_payoff = (i, j, cells[i, j].sum_payoff)
        for k in range(i - 1, i + 2):
            for n in range(j - 1, j + 2):
                if k == i and n == j:
                    continue
                if max_payoff[2] < cells[k, n].sum_payoff:
                    max_payoff = (k, n, cells[k, n].sum_payoff)
        k, n, payoff = max_payoff
        cells[i, j].winner_agent = cells[k, n].id
        if k != i or n != j:
            cells_temp[i, j].strategy = cells[k, n].strategy
            cells_temp[i, j].k = cells[k, n].k
            return True
        return False

    # roulette competition - neighbour with the highest payoff has the highest probability to win

    def roulette_competition(self, cells, cells_temp, i, j):
        payoffs = []
        sum_of_payoffs = 0
        for k in range(i - 1, i + 2):
            for n in range(j - 1, j + 2):
                payoffs.append((k, n, cells[k, n].sum_payoff))
                sum_of_payoffs += cells[k, n].sum_payoff
        probabilities = [(k, n, payoff / sum_of_payoffs) for k, n, payoff in payoffs]
        probabilities_standardized = []
        sum_probabilities = 0
        for k, n, probability in probabilities:
            sum_probabilities += probability
            probabilities_standardized.append((k, n, sum_probabilities))
        x = random.random()
        for k, n, probability in probabilities_standardized:
            if x <= probability:
                if k != i or n != j:
                    cells_temp[i, j].strategy = cells[k, n].strategy
                    cells_temp[i, j].k = cells[k, n].k
                    return True
                return False

    def redistribute_payoff(self, cells, cells_temp, i, j):
        cells[i, j].pay_to_send = cells_temp[i, j].avg_payoff/9
        cells[i, j].pay_to_receive = 0.0
        for k in range(i - 1, i + 2):
            for n in range(j - 1, j + 2):
                if k == i and j == n:
                    continue
                cells[i, j].pay_to_receive += cells_temp[k, n].avg_payoff/9
        cells[i, j].avg_payoff = cells[i, j].pay_to_send + cells[i, j].pay_to_receive
        for k in range(8):
            cells[i, j].payoffs[k] = cells[i, j].avg_payoff
        cells[i, j].sum_payoff = 8 * cells[i, j].avg_payoff

    def calculate_payoff(self, cells, i, j):
        # action is D
        m = 0
        if cells[i, j].action == 0:
            # if cell is in group_of_1s or group_of_0s then all cells in neighbourhood have action = D (= 0)
            # for loop over cell's neighbours
            for k in range(i - 1, i + 2):
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
            for k in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if k == i and j == n:
                        continue
                    if cells[k, n].action == 1:
                        cells[i, j].payoffs[m] = self.payoff_C_C
                        cells[i, j].sum_payoff += self.payoff_C_C
                    elif cells[k, n].action == 0:
                        cells[i, j].payoffs[m] = self.payoff_C_D
                        cells[i, j].sum_payoff += self.payoff_C_D
                    m += 1
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

    def is_cell_changing_strategy(self, cell):
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
            num_of_0D = num_of_1D = num_of_2D = num_of_3D = num_of_4D = num_of_5D = num_of_6D = num_of_7D = num_of_8D = 0
            num_of_0C = num_of_1C = num_of_2C = num_of_3C = num_of_4C = num_of_5C = num_of_6C = num_of_7C = num_of_8C = 0
            num_of_0DC = num_of_1DC = num_of_2DC = num_of_3DC = num_of_4DC = num_of_5DC = num_of_6DC = num_of_7DC = num_of_8DC = 0
            num_of_group_0s = num_of_group_1s = 0

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
                    if cells[i, j].group_of_1s:
                        num_of_group_1s += 1
                    elif cells[i, j].group_of_0s:
                        num_of_group_0s += 1

            # calculate the stats
            f_C = num_of_C / num_of_cells
            f_C_corr = num_of_C_corr / self.optimal_num_1s
            iter1, av_sum = self.avg_payoff[k]
            f_allC = num_of_allC / num_of_cells
            f_allD = num_of_allD / num_of_cells
            f_kD = num_of_kD / num_of_cells
            f_kC = num_of_kC / num_of_cells
            f_kDC = num_of_kDC / num_of_cells

            _, num_of_strat_change, num_of_strat_change_final = self.misc_stats[k]
            f_strat_ch = num_of_strat_change / num_of_cells
            f_strat_ch_final = num_of_strat_change_final / num_of_cells
            f_cr_0s = num_of_group_0s / num_of_cells
            f_cr_1s = num_of_group_1s / num_of_cells

            # if num_of_kD = 0 then num_of_XD (X = 0, 1...) also = 0, so the division should be = 0
            # adding 1 to make it so
            if num_of_kD == 0:
                num_of_kD = 1
            f_0D = num_of_0D / num_of_kD
            f_1D = num_of_1D / num_of_kD
            f_2D = num_of_2D / num_of_kD
            f_3D = num_of_3D / num_of_kD
            f_4D = num_of_4D / num_of_kD
            f_5D = num_of_5D / num_of_kD
            f_6D = num_of_6D / num_of_kD
            f_7D = num_of_7D / num_of_kD
            f_8D = num_of_8D / num_of_kD

            if num_of_kC == 0:
                num_of_kC = 1
            f_0C = num_of_0C / num_of_kC
            f_1C = num_of_1C / num_of_kC
            f_2C = num_of_2C / num_of_kC
            f_3C = num_of_3C / num_of_kC
            f_4C = num_of_4C / num_of_kC
            f_5C = num_of_5C / num_of_kC
            f_6C = num_of_6C / num_of_kC
            f_7C = num_of_7C / num_of_kC
            f_8C = num_of_8C / num_of_kC

            if num_of_kDC == 0:
                num_of_kDC = 1
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
                                          f_0DC, f_1DC, f_2DC, f_3DC, f_4DC, f_5DC, f_6DC, f_7DC, f_8DC,
                                          f_strat_ch_final, f_cr_0s, f_cr_1s)))
        return statistics
