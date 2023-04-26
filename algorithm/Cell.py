# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:30:18 2023

@author: pozdro
"""
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import (QBrush, QColor)
import numpy as np

class Cell(QTableWidgetItem):
    def __init__(self, _id, x, y, strategy = -1, k = -1, action = -1, state = -1):
        
        
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
        
        # not yet sure if necessary...
        # self.my_neighb_states = np.empty(8, dtype=int)
        # self.payoffs = np.empty(8, dtype=int)
        
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

        
