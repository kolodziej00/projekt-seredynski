# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:30:18 2023

@author: pozdro
"""
import copy

from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import (QBrush, QColor)
import numpy as np

class Cell(QTableWidgetItem):
    def __init__(self, _id, x, y, strategy = -1, k = -1, action = -1, state = -1, group_of_1s = False, group_of_0s = False, change_strategy = False):
        super().__init__()
        super().__init_subclass__()

        # strategy of Cell - decides cell's state in next step of Cellular automata
        # 0 - all D - always defect (state = 0)
        # 1 - all C - always coperate (state = 1)
        # 2 - kD - cooperate until no more than K neighbours defect, otherwise defect
        # 3 - kC - cooperate until no more than K neighbours cooperate, otherwise defect
        # 4 - kDC - defect until not more than K neighbors defect, otherwise cooperate 
        self.strategy = strategy
        self.state = state
        self.k = k
        
        # action depends on cell's state and states of neighbours i.e. if cell's neighbourhood (including the cell) is correct
        # then action=1 (cooperate) otherwise action=0 (defect)
        self.action = action
        
        # coordinates in cellular automata
        self.x = x
        self.y = y
        # global ID 
        self.id = _id

        self.group_of_1s = group_of_1s
        self.group_of_0s = group_of_0s
        self.change_strategy = change_strategy

        # cell's payoff in game with each neighbour [0] - north neighbour, [1] - north-west, [2] - west, [3] - south-west,
        # [4] - south, [5] - south-east, [6] - east, [7] - north
        self.payoffs = np.empty(8, dtype=float)
        self.sum_payoff = 0
        self.avg_payoff = 0



    def __deepcopy__(self, memodict={}):
        return Cell(self.id, self.x, self.y, self.strategy, self.k, self.action, self.state, self.group_of_1s, self.group_of_0s,
                    self.change_strategy)

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

        
