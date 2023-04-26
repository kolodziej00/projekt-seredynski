# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 10:35:46 2023

@author: pozdro
"""
import math

from PySide6.QtWidgets import (QMainWindow, QTableWidgetItem)
from PySide6.QtCore import QRect
from GUI.ui_mainwindow import Ui_MainWindow

from data.canvas import Canvas
from data.competition import Competition
from data.debugger import Debugger
from data.iterations import Iterations
from data.mutation import Mutation
from data.myData import MyData
from data.seed import Seed
from data.strategies import Strategies
from data.synch import Synch

from algorithm.Cell import Cell

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def roundDivision(self, size, n):
        floor = math.floor(size / n)
        roof = math.ceil(size / n)
        floorDif = abs(size - floor * n)
        roofDif = abs(size - roof * n)
        if floorDif < roofDif:
            return floor
        else:
            return roof

    def createTableCA(self):
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        self.ui.graphicsView_CA.setRowCount(rows)
        self.ui.graphicsView_CA.setColumnCount(cols)
        for n in range(rows):
            for m in range(cols):
                # Tutaj później zamienić QTableWidgetItem na Cell
                self.ui.graphicsView_CA.setItem(n, m, QTableWidgetItem())
        cellWidth = self.roundDivision(self.ui.graphicsView_CA.width(), cols)
        cellHeight = self.roundDivision(self.ui.graphicsView_CA.height(), rows)
        width = cellWidth * cols + 2
        height = cellHeight * rows + 2
        self.ui.graphicsView_CA.setGeometry(QRect(490, 80, width, height))
        self.ui.graphicsView_CA.horizontalHeader().setDefaultSectionSize(cellWidth)
        self.ui.graphicsView_CA.verticalHeader().setDefaultSectionSize(cellHeight)
             

    def setData(self):
        self.data = MyData(self.canvas, self.competition, self.debugger,
                         self.iterations, self.mutation, self.seed,
                         self.strategies, self.synch)
        self.createTableCA()

    def startSimulation(self):
        self.canvas = Canvas(self.ui.spinBox_Mrows.value(), 
                                self.ui.spinBox_Ncols.value(), 
                                self.ui.doubleSpinBox_p_init_C.value(),
                                self.ui.checkBox_sharing.isChecked())
        
        self.competition = Competition(self.ui.radioButton_roulette.isChecked(),
                                        self.ui.radioButton_tournament.isChecked())
        
        self.debugger = Debugger(self.ui.groupBox_debug.isChecked(),
                                    self.ui.radioButton_CA_state.isChecked(), 
                                    self.ui.radioButton_CA_strat.isChecked())
        
        self.iterations = Iterations(self.ui.spinBox_num_of_iter.value(),
                                        self.ui.spinBox_num_of_exper.value())
        
        self.mutation = Mutation(self.ui.doubleSpinBox_p_state_mut.value(), 
                                    self.ui.doubleSpinBox_p_strat_mut.value(),
                                    self.ui.doubleSpinBox_p_0_neigh_mut.value(), 
                                    self.ui.doubleSpinBox_p_1_neigh_mut.value())
        
        self.seed = Seed(self.ui.radioButton_clock.isChecked(),
                            self.ui.radioButton_custom.isChecked(), 
                            self.ui.spinBox_custom_seed.value())
        
        self.synch = Synch(self.ui.doubleSpinBox_synch_prob.value(), 
                            self.ui.spinBox_optimal_num_1s.value())
        
        self.strategies = Strategies(self.ui.doubleSpinBox_allC.value(), 
                                        self.ui.doubleSpinBox_allD.value(), 
                                        self.ui.doubleSpinBox_kD.value(), 
                                        self.ui.doubleSpinBox_kC.value(), 
                                        self.ui.doubleSpinBox_kDC.value(), 
                                        self.ui.spinBox_kMin.value(),
                                        self.ui.spinBox_kMax.value())
        self.setData()
                        

            
