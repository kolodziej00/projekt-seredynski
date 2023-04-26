# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:30:18 2023

@author: pozdro
"""
from PySide6.QtWidgets import QTableWidgetItem
import numpy as np

class Cell(QTableWidgetItem):
    def __init__(self, _id, x, y, strategy = -1, k = -1, action = -1, state = -1):
        self.strategy = strategy
        self.state = state
        self.k = k
        self.action = action
        self.x = x
        self.y = y
        self.id = _id
        self.my_neighb_states = np.empty(8, dtype=int)
        self.payoffs = np.empty(8, dtype=int)
        
