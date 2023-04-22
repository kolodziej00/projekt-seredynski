# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:29:46 2023

@author: pozdro
"""
import random
import numpy as np
from algorithm.Cell import Cell
class CA:
    def __init__(self, M_rows, N_cols, p_init_C, allC, allD, kD, kC, minK, maxK, seed = None):
        self.M_rows = M_rows
        self.N_cols = N_cols
        if seed == None:
            random.seed()
        else:
            random.seed(seed)
        self.CA_cells = self.create_CA(p_init_C, allC, allD, kD, kC, minK, maxK)
        
        
    
    def create_CA(self, p_init_C, allC, allD, kD, kC, minK, maxK):
        CA_cells = np.empty((self.M_rows, self.N_cols), dtype=object)
        id_ = 0
        for i in range(0, self.M_rows):
            for j in range(0, self.N_cols):
                # Cells on borders have predefined static properties.
                if i == 0 or i == self.M_rows - 1 or j == 0 or j == self.N_cols - 1:
                    CA_cells[i,j] = Cell(_id = id_, x =j , y = i, state = 0, action = 1, strategy = 0)
                else:
                # the rest of cells have randomly assigned states and strategies
                    state = self.init_cell_state( p_init_C)
                    strategy, k = self.init_cell_strategy(allC, allD, kD, kC, minK, maxK)
                    CA_cells[i,j] = Cell(_id = id_, x = j, y = i, strategy = strategy, k = k, state = state)
                id_ += 1
        return CA_cells
    
    def init_cell_state(self, p_init_C):
            x = random.random()
            if x <= p_init_C:
                state = 1
            else:
                state = 0
            return state
                    
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
                