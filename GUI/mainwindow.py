# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 10:35:46 2023

@author: pozdro
"""
import math

from PySide6.QtWidgets import (QMainWindow, QTableWidgetItem, QMessageBox)
from PySide6.QtGui import (QColor, QPixmap)
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

from algorithm.CA import CA

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def displayDataWarning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Can't process data.\nThe data entered is incorrect.")
        msg.setWindowTitle("Invalid input")
        msg.exec_()

    def saveImage(self):
        pixmap = QPixmap(self.ui.graphicsView_CA.size())
        self.ui.graphicsView_CA.render(pixmap)
        fileName = "Images//image" + str(self.ui.lcdNumber_iters.value()) + ".png"
        pixmap.save(fileName, "PNG", -1)

    def changeCellsColor(self, selected, R, G, B):
        for ix in selected:
            row, column = ix
            self.ui.graphicsView_CA.item(row, column).setBackground(QColor(R,G,B, 255))
                
                
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
        self.automata = CA(rows, cols, self.data.canvas.p_init_C, self.data.strategies.all_C,
                       self.data.strategies.all_D, self.data.strategies.k_D, self.data.strategies.k_C,
                       self.data.strategies.k_var_min, self.data.strategies.k_var_max, None)
        for n in range(rows):
            for m in range(cols):
                self.ui.graphicsView_CA.setItem(n, m, self.automata.cells[n, m])
                if self.automata.cells[n,m].state==1:
                    self.ui.graphicsView_CA.item(n,m).setBackground(QColor(255,100,0,255))
        cellWidth = self.roundDivision(300, cols)
        cellHeight = self.roundDivision(300, rows)
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
        #Tutaj należy sprawdzić wszystkie wprowadzone dane zanim zostaną one przekazane dalej
        allC = self.ui.doubleSpinBox_allC.value()
        allD = self.ui.doubleSpinBox_allD.value()
        kD = self.ui.doubleSpinBox_kD.value()
        kC = self.ui.doubleSpinBox_kC.value()
        kDC = self.ui.doubleSpinBox_kDC.value()
        strategySum = allC + allD + kD + kC + kDC
        if strategySum != 1:
            self.displayDataWarning()
            return

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
        
        self.ui.pushButton_states.setDisabled(0)
        self.ui.pushButton_strategies.setDisabled(0)
        self.ui.pushButton_kD.setDisabled(0)
        self.ui.pushButton_kC.setDisabled(0)
        self.ui.pushButton_kDC.setDisabled(0)
        self.ui.pushButton_actions.setDisabled(0)
        self.ui.pushButton_states.setDisabled(0)
        
    
    def state_color_handler(self):
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        selected = []
        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(255,255,255, 255))
                if self.automata.cells[i,j].state==1:
                    selected.append((i,j))
        self.changeCellsColor(selected, 255, 100, 0)      
        
    def strategies_color_handler(self):
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        selected_all_C = []
        selected_all_D = []
        selected_kD = []
        selected_kC = []
        selected_kDC = []
        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(255,255,255, 255))
                if self.automata.cells[i,j].strategy==0:
                    selected_all_D.append((i,j))
                elif self.automata.cells[i,j].strategy==1:
                    selected_all_C.append((i,j))
                elif self.automata.cells[i,j].strategy==2:
                    selected_kD.append((i,j))
                elif self.automata.cells[i,j].strategy==3:
                    selected_kC.append((i,j))
                elif self.automata.cells[i,j].strategy==4:
                    selected_kDC.append((i,j))
        
        self.changeCellsColor(selected_all_C, 255, 100, 0) # red
        self.changeCellsColor(selected_all_D, 0,0,255) # blue
        self.changeCellsColor(selected_kD, 0,128,0) # green
        self.changeCellsColor(selected_kC, 0,255,255) # cyan
        self.changeCellsColor(selected_kDC, 255,20,147) # pink
                   
        
