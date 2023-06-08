# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 10:35:46 2023

@author: pozdro
"""
import datetime
import math
import time
import asyncio

from PySide6.QtWidgets import (QMainWindow, QTableWidgetItem, QMessageBox)
from PySide6.QtGui import (QColor, QPixmap)
from PySide6.QtCore import (QRect, QThreadPool, QMutex)
from GUI.ui_mainwindow import Ui_MainWindow
from PySide6.QtGui import (QPen)


from data.canvas import Canvas
from data.competition import Competition
from data.debugger import Debugger
from data.iterations import Iterations
from data.mutation import Mutation
from data.myData import MyData
from data.seed import Seed
from data.strategies import Strategies
from data.synch import Synch
from data.payoff import Payoff

from algorithm.CA import CA
from GUI.animation import Animation
from algorithm.StatisticsMultirun import StatisticsMultirun
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()
        self.mutex = QMutex()
        self.isAnimationRunning = False
        self.visualization_mode = 0

    def resetIterations(self):
        print("Reset iteracji")
        self.ui.spinBox_num_of_iter.value = 0

    def displayDataWarning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Can't process data.\nThe data entered is incorrect.")
        msg.setWindowTitle("Invalid input")
        msg.exec_()

    def saveImage(self):
        pixmap = QPixmap(self.ui.graphicsView_CA.size())
        self.ui.graphicsView_CA.render(pixmap)
        fileName = "Images//image" + str(self.ui.lcdNumber_iters.value()) + str(self.visualization_mode) + ".png"
        pixmap.save(fileName, "PNG", -1)
        



    def changeCellsColor(self, selected, R, G, B, opacity=255):
        tasks=[]
        for ix in selected:
            row, column = ix
            tasks.append(asyncio.to_thread(self.ui.graphicsView_CA.item(row, column).setBackground(QColor(R,G,B, opacity))))
        try:
            asyncio.run(asyncio.gather(*tasks) )
        except:
            pass
                
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
        if self.seed.isCustomSeed:
            seed = self.seed.customSeed
        else:
            seed = None
        f = open("outputs.txt", "w")
        self.automata = CA(rows, cols, self.data.canvas.p_init_C, self.data.strategies.all_C,
                           self.data.strategies.all_D, self.data.strategies.k_D, self.data.strategies.k_C,
                           self.data.strategies.k_var_min, self.data.strategies.k_var_max, self.data.iterations.num_of_iter,
                           self.data.payoff.d, self.data.payoff.c, self.data.payoff.b, self.data.payoff.a, self.canvas.isSharing,
                           self.data.synch.synch_prob, self.data.competition.isTournament, self.data.mutations.p_state_mut,
                           self.data.mutations.p_strat_mut, self.data.mutations.p_0_neighb_mut, self.data.mutations.p_1_neighb_mut,
                           self.data.debugger.isDebug, self.data.debugger.is_test1, self.data.debugger.is_test2, f,
                           self.data.synch.optimal_num_1s,
                           seed)

        k, cells = self.automata.cells[0]
        for n in range(rows):
            for m in range(cols):
                self.ui.graphicsView_CA.setItem(n, m, cells[n, m])
                if cells[n, m].state == 1:
                        self.ui.graphicsView_CA.item(n, m).setBackground(QColor(255, 100, 0, 255))
        cellWidth = self.roundDivision(300, cols)
        cellHeight = self.roundDivision(300, rows)
        width = cellWidth * cols + 2
        height = cellHeight * rows + 2
        self.ui.graphicsView_CA.setGeometry(QRect(490, 80, width, height))
        self.ui.graphicsView_CA.horizontalHeader().setDefaultSectionSize(cellWidth)
        self.ui.graphicsView_CA.verticalHeader().setDefaultSectionSize(cellHeight)

        self.create_coloring()



    def create_coloring(self):
        self.coloring_state = []
        self.coloring_allC = []
        self.coloring_allD = []
        self.coloring_kD = []
        self.coloring_kC = []
        self.coloring_kDC = []

        self.coloring_kD_0 = []
        self.coloring_kD_1 = []
        self.coloring_kD_2 = []
        self.coloring_kD_3 = []
        self.coloring_kD_4 = []
        self.coloring_kD_5 = []
        self.coloring_kD_6 = []
        self.coloring_kD_7 = []
        self.coloring_kD_8 = []

        self.coloring_kC_0 = []
        self.coloring_kC_1 = []
        self.coloring_kC_2 = []
        self.coloring_kC_3 = []
        self.coloring_kC_4 = []
        self.coloring_kC_5 = []
        self.coloring_kC_6 = []
        self.coloring_kC_7 = []
        self.coloring_kC_8 = []

        self.coloring_kDC_0 = []
        self.coloring_kDC_1 = []
        self.coloring_kDC_2 = []
        self.coloring_kDC_3 = []
        self.coloring_kDC_4 = []
        self.coloring_kDC_5 = []
        self.coloring_kDC_6 = []
        self.coloring_kDC_7 = []
        self.coloring_kDC_8 = []
        self.coloring_actions = []

        rows = self.data.canvas.rows
        cols = self.data.canvas.cols

        for iter, cells in self.automata.cells:

            coloring_state_temp = []
            coloring_allD_temp = []
            coloring_allC_temp = []
            coloring_kD_temp = []
            coloring_kC_temp = []
            coloring_kDC_temp = []
            coloring_kD_0_temp = []
            coloring_kD_1_temp = []
            coloring_kD_2_temp = []
            coloring_kD_3_temp = []
            coloring_kD_4_temp = []
            coloring_kD_5_temp = []
            coloring_kD_6_temp = []
            coloring_kD_7_temp = []
            coloring_kD_8_temp = []
            coloring_kC_0_temp = []
            coloring_kC_1_temp = []
            coloring_kC_2_temp = []
            coloring_kC_3_temp = []
            coloring_kC_4_temp = []
            coloring_kC_5_temp = []
            coloring_kC_6_temp = []
            coloring_kC_7_temp = []
            coloring_kC_8_temp = []
            coloring_kDC_0_temp = []
            coloring_kDC_1_temp = []
            coloring_kDC_2_temp = []
            coloring_kDC_3_temp = []
            coloring_kDC_4_temp = []
            coloring_kDC_5_temp = []
            coloring_kDC_6_temp = []
            coloring_kDC_7_temp = []
            coloring_kDC_8_temp = []
            coloring_actions_temp = []
            for i in range(rows):
                for j in range(cols):
                    # state coloring
                    if cells[i, j].state == 1:
                        coloring_state_temp.append((i, j))
                        # all D
                    if cells[i, j].strategy == 0:
                        coloring_allD_temp.append((i, j))
                        # all C
                    elif cells[i, j].strategy == 1:
                        coloring_allC_temp.append((i, j))
                        # kD
                    elif cells[i, j].strategy == 2:
                        coloring_kD_temp.append((i, j))
                        if cells[i, j].k == 0:
                            coloring_kD_0_temp.append((i, j))
                        elif cells[i, j].k == 1:
                            coloring_kD_1_temp.append((i, j))
                        elif cells[i, j].k == 2:
                            coloring_kD_2_temp.append((i, j))
                        elif cells[i, j].k == 3:
                            coloring_kD_3_temp.append((i, j))
                        elif cells[i, j].k == 4:
                            coloring_kD_4_temp.append((i, j))
                        elif cells[i, j].k == 5:
                            coloring_kD_5_temp.append((i, j))
                        elif cells[i, j].k == 6:
                            coloring_kD_6_temp.append((i, j))
                        elif cells[i, j].k == 7:
                            coloring_kD_7_temp.append((i, j))
                        elif cells[i, j].k == 8:
                            coloring_kD_8_temp.append((i, j))
                        # kC
                    elif cells[i, j].strategy == 3:
                        coloring_kC_temp.append((i, j))
                        if cells[i, j].k == 0:
                            coloring_kC_0_temp.append((i, j))
                        elif cells[i, j].k == 1:
                            coloring_kC_1_temp.append((i, j))
                        elif cells[i, j].k == 2:
                            coloring_kC_2_temp.append((i, j))
                        elif cells[i, j].k == 3:
                            coloring_kC_3_temp.append((i, j))
                        elif cells[i, j].k == 4:
                            coloring_kC_4_temp.append((i, j))
                        elif cells[i, j].k == 5:
                            coloring_kC_5_temp.append((i, j))
                        elif cells[i, j].k == 6:
                            coloring_kC_6_temp.append((i, j))
                        elif cells[i, j].k == 7:
                            coloring_kC_7_temp.append((i, j))
                        elif cells[i, j].k == 8:
                            coloring_kC_8_temp.append((i, j))
                        # kDC
                    elif cells[i, j].strategy == 4:
                        coloring_kDC_temp.append((i, j))
                        if cells[i, j].k == 0:
                            coloring_kDC_0_temp.append((i, j))
                        elif cells[i, j].k == 1:
                            coloring_kDC_1_temp.append((i, j))
                        elif cells[i, j].k == 2:
                            coloring_kDC_2_temp.append((i, j))
                        elif cells[i, j].k == 3:
                            coloring_kDC_3_temp.append((i, j))
                        elif cells[i, j].k == 4:
                            coloring_kDC_4_temp.append((i, j))
                        elif cells[i, j].k == 5:
                            coloring_kDC_5_temp.append((i, j))
                        elif cells[i, j].k == 6:
                            coloring_kDC_6_temp.append((i, j))
                        elif cells[i, j].k == 7:
                            coloring_kDC_7_temp.append((i, j))
                        elif cells[i, j].k == 8:
                            coloring_kDC_8_temp.append((i, j))
                    if cells[i, j].action == 1:
                        coloring_actions_temp.append((i, j))

            self.coloring_state.append(coloring_state_temp)
            self.coloring_allC.append(coloring_allC_temp)
            self.coloring_allD.append(coloring_allD_temp)
            self.coloring_kD.append(coloring_kD_temp)
            self.coloring_kC.append(coloring_kC_temp)
            self.coloring_kDC.append(coloring_kDC_temp)
            self.coloring_kD_0.append(coloring_kD_0_temp)
            self.coloring_kD_1.append(coloring_kD_1_temp)
            self.coloring_kD_2.append(coloring_kD_2_temp)
            self.coloring_kD_3.append(coloring_kD_3_temp)
            self.coloring_kD_4.append( coloring_kD_4_temp)
            self.coloring_kD_5.append(coloring_kD_5_temp)
            self.coloring_kD_6.append(coloring_kD_6_temp)
            self.coloring_kD_7.append(coloring_kD_7_temp)
            self.coloring_kD_8.append(coloring_kD_8_temp)
            self.coloring_kC_0.append(coloring_kC_0_temp)
            self.coloring_kC_1.append(coloring_kC_1_temp)
            self.coloring_kC_2.append(coloring_kC_2_temp)
            self.coloring_kC_3.append(coloring_kC_3_temp)
            self.coloring_kC_4.append(coloring_kC_4_temp)
            self.coloring_kC_5.append(coloring_kC_5_temp)
            self.coloring_kC_6.append(coloring_kC_6_temp)
            self.coloring_kC_7.append(coloring_kC_7_temp)
            self.coloring_kC_8.append(coloring_kC_8_temp)
            self.coloring_kDC_0.append(coloring_kDC_0_temp)
            self.coloring_kDC_1.append(coloring_kDC_1_temp)
            self.coloring_kDC_2.append(coloring_kDC_2_temp)
            self.coloring_kDC_3.append(coloring_kDC_3_temp)
            self.coloring_kDC_4.append(coloring_kDC_4_temp)
            self.coloring_kDC_5.append(coloring_kDC_5_temp)
            self.coloring_kDC_6.append(coloring_kDC_6_temp)
            self.coloring_kDC_7.append(coloring_kDC_7_temp)
            self.coloring_kDC_8.append(coloring_kDC_8_temp)
            self.coloring_actions.append(coloring_actions_temp)


    def setData(self):
        self.data = MyData(self.canvas, self.competition, self.debugger,
                         self.iterations, self.mutation, self.seed,
                         self.strategies, self.synch, self.payoff)
        self.createTableCA()

    def closeRunningThreads(self):
        # Terminating running threads
        if self.isAnimationRunning == True:
            if self.animation.stillRunning():
                self.animation.terminate()
            self.isAnimationRunning = False
            self.ui.spinBox_iters.setValue(0)

    def startSimulation(self):
        self.closeRunningThreads()

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
        
        self.debugger = Debugger(self.ui.radioButton_debug.isChecked(),
                                    self.ui.radioButton_CA_state.isChecked(), 
                                    self.ui.radioButton_CA_strat.isChecked(),
                                 self.ui.radioButton_test1.isChecked(), self.ui.radioButton_test2.isChecked(),
                                 self.ui.radioButton_test3.isChecked())
        
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

        self.payoff = Payoff(self.ui.doubleSpinBox_a.value(),
                             self.ui.doubleSpinBox_b.value(),
                             self.ui.doubleSpinBox_c.value(),
                             self.ui.doubleSpinBox_d.value())
        self.ui.spinBox_iters.setMaximum(self.iterations.num_of_iter-1)
        self.visualization_mode = 0  # state visualization
        self.setData()
        
        self.ui.pushButton_states.setDisabled(0)
        self.ui.pushButton_strategies.setDisabled(0)
        self.ui.pushButton_kD.setDisabled(0)
        self.ui.pushButton_kC.setDisabled(0)
        self.ui.pushButton_kDC.setDisabled(0)
        self.ui.pushButton_actions.setDisabled(0)
        self.ui.pushButton_states.setDisabled(0)

        self.save_results()

    def state_color_handler(self):
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        iter = self.ui.spinBox_iters.value()

        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(255, 255, 255, 255))

        self.changeCellsColor(self.coloring_state[iter], 255, 100, 0)
        self.visualization_mode = 0
        
        
    def strategies_color_handler(self):
        # if self.isAnimationRunning == True:
        #     self.animation.extendSleepTime()
            
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        iter = self.ui.spinBox_iters.value()

        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(255, 255, 255, 255))
        
        self.changeCellsColor(self.coloring_allC[iter], 255, 100, 0)  # red
        self.changeCellsColor(self.coloring_allD[iter], 0, 0, 255)  # blue
        self.changeCellsColor(self.coloring_kD[iter], 0, 128, 0)  # green
        self.changeCellsColor(self.coloring_kC[iter], 0, 255, 255)  # cyan
        self.changeCellsColor(self.coloring_kDC[iter], 255, 20, 147)  # pink
        self.visualization_mode = 1

    def kD_strategies_color_handler(self):
        # if self.isAnimationRunning == True:
        #     self.animation.extendSleepTime()

        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        iter = self.ui.spinBox_iters.value()

        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(0, 0, 0, 255))

        self.changeCellsColor(self.coloring_kD_0[iter], 0, 128, 0, 0)
        self.changeCellsColor(self.coloring_kD_1[iter], 0, 128, 0, 31)
        self.changeCellsColor(self.coloring_kD_2[iter], 0, 128, 0, 62)
        self.changeCellsColor(self.coloring_kD_3[iter], 0, 128, 0, 93)
        self.changeCellsColor(self.coloring_kD_4[iter], 0, 128, 0, 124)
        self.changeCellsColor(self.coloring_kD_5[iter], 0, 128, 0, 156)
        self.changeCellsColor(self.coloring_kD_6[iter], 0, 128, 0, 187)
        self.changeCellsColor(self.coloring_kD_7[iter], 0, 128, 0, 218)
        self.changeCellsColor(self.coloring_kD_8[iter], 0, 128, 0, 255)

        self.visualization_mode = 2

    def kC_strategies_color_handler(self):
        # if self.isAnimationRunning == True:
        #     self.animation.extendSleepTime()
        
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        iter = self.ui.spinBox_iters.value()

        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(0, 0, 0, 200))

        self.changeCellsColor(self.coloring_kC_0[iter], 0, 255, 255, 0)
        self.changeCellsColor(self.coloring_kC_1[iter], 0, 255, 255, 31)
        self.changeCellsColor(self.coloring_kC_2[iter], 0, 255, 255, 62)
        self.changeCellsColor(self.coloring_kC_3[iter], 0, 255, 255, 93)
        self.changeCellsColor(self.coloring_kC_4[iter], 0, 255, 255, 124)
        self.changeCellsColor(self.coloring_kC_5[iter], 0, 255, 255, 156)
        self.changeCellsColor(self.coloring_kC_6[iter], 0, 255, 255, 187)
        self.changeCellsColor(self.coloring_kC_7[iter], 0, 255, 255, 218)
        self.changeCellsColor(self.coloring_kC_8[iter], 0, 255, 255, 255)

        self.visualization_mode = 3

    def kDC_strategies_color_handler(self):
        # if self.isAnimationRunning == True:
        #     self.animation.extendSleepTime()

        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        iter = self.ui.spinBox_iters.value()

        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(0, 0, 0, 200))

        self.changeCellsColor(self.coloring_kDC_0[iter], 255, 20, 147, 0)
        self.changeCellsColor(self.coloring_kDC_1[iter], 255, 20, 147, 31)
        self.changeCellsColor(self.coloring_kDC_2[iter], 255, 20, 147, 62)
        self.changeCellsColor(self.coloring_kDC_3[iter], 255, 20, 147, 93)
        self.changeCellsColor(self.coloring_kDC_4[iter], 255, 20, 147, 124)
        self.changeCellsColor(self.coloring_kDC_5[iter], 255, 20, 147, 156)
        self.changeCellsColor(self.coloring_kDC_6[iter], 255, 20, 147, 187)
        self.changeCellsColor(self.coloring_kDC_7[iter], 255, 20, 147, 218)
        self.changeCellsColor(self.coloring_kDC_8[iter], 255, 20, 147, 255)

        self.visualization_mode = 4

    def action_color_handler(self):
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        iter = self.ui.spinBox_iters.value()
        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(0, 0, 255, 255))
        self.changeCellsColor(self.coloring_actions[iter], 255, 100, 0)
        self.visualization_mode = 5
        


    def save_results(self):
        f = open("result-a.txt", "w")
        f2 = open("result-b.txt", "w")

        # result-a
        f.write("#num_of_iter: " + str(self.data.iterations.num_of_iter))
        f.write("\n#num_of_exper: " + str(self.data.iterations.num_of_exper))
        f.write("\n#rows: " + str(self.data.canvas.rows))
        f.write("\n#cols: " + str(self.data.canvas.cols))
        f.write("\n#p_init_C: " + str(self.data.canvas.p_init_C))
        f.write("\n#p_state_mut: " + str(self.data.mutations.p_state_mut))
        f.write("\n#p_strat_mut: " + str(self.data.mutations.p_strat_mut))
        f.write("\n#p_0_neighb: " + str(self.data.mutations.p_0_neighb_mut))
        f.write("\n#p_1_neighb: " + str(self.data.mutations.p_1_neighb_mut))
        if(self.data.competition.isRoulette):
            f.write("\n#comp_type: roulette")
        elif(self.data.competition.isTournament):
            f.write("\n#comp_type: tournament")
        else:
            f.write("\n#comp_type: None?")

        f.write("\n#sharing: " + str(self.data.canvas.isSharing))
        f.write("\n#allC: " + str(self.data.strategies.all_C))
        f.write("\n#allD: " + str(self.data.strategies.all_D))
        f.write("\n#kD: " + str(self.data.strategies.k_D))
        f.write("\n#kC: " + str(self.data.strategies.k_C))
        f.write("\n#kDC: " + str(self.data.strategies.k_DC))
        f.write("\n#k_values: " + str(self.data.strategies.k_var_min) + " to " + str(self.data.strategies.k_var_max))
        f.write("\n#synchronity_prob: " + str(self.data.synch.synch_prob))
        f.write("\n#optimal_num_of_1s: " + str(self.data.synch.optimal_num_1s))
        f.write("\n#playerC_opponentD_payoff: " + str(self.data.payoff.c))
        f.write("\n#playerC_opponentC_payoff: " + str(self.data.payoff.d))
        f.write("\n#playerD_opponentD_payoff: " + str(self.data.payoff.a))
        f.write("\n#playerD_opponentC_payoff: " + str(self.data.payoff.b))
        f.write("\n#debug:  " + str(self.data.debugger.isDebug))
        #########

        # result-b
        f2.write("#num_of_iter: " + str(self.data.iterations.num_of_iter))
        f2.write("\n#num_of_exper: " + str(self.data.iterations.num_of_exper))
        f2.write("\n#rows: " + str(self.data.canvas.rows))
        f2.write("\n#cols: " + str(self.data.canvas.cols))
        f2.write("\n#p_init_C: " + str(self.data.canvas.p_init_C))
        f2.write("\n#p_state_mut: " + str(self.data.mutations.p_state_mut))
        f2.write("\n#p_strat_mut: " + str(self.data.mutations.p_strat_mut))
        f2.write("\n#p_0_neighb: " + str(self.data.mutations.p_0_neighb_mut))
        f2.write("\n#p_1_neighb: " + str(self.data.mutations.p_1_neighb_mut))
        if(self.data.competition.isRoulette):
            f2.write("\n#comp_type: roulette")
        elif(self.data.competition.isTournament):
            f2.write("\n#comp_type: tournament")
        else:
            f2.write("\n#comp_type: None?")

        f2.write("\n#sharing: " + str(self.data.canvas.isSharing))
        f2.write("\n#allC: " + str(self.data.strategies.all_C))
        f2.write("\n#allD: " + str(self.data.strategies.all_D))
        f2.write("\n#kD: " + str(self.data.strategies.k_D))
        f2.write("\n#kC: " + str(self.data.strategies.k_C))
        f2.write("\n#kDC: " + str(self.data.strategies.k_DC))
        f2.write("\n#k_values: " + str(self.data.strategies.k_var_min) + " to " + str(self.data.strategies.k_var_max))
        f2.write("\n#synchronity_prob: " + str(self.data.synch.synch_prob))
        f2.write("\n#optimal_num_of_1s: " + str(self.data.synch.optimal_num_1s))
        f2.write("\n#playerC_opponentD_payoff: " + str(self.data.payoff.c))
        f2.write("\n#playerC_opponentC_payoff: " + str(self.data.payoff.d))
        f2.write("\n#playerD_opponentD_payoff: " + str(self.data.payoff.a))
        f2.write("\n#playerD_opponentC_payoff: " + str(self.data.payoff.b))
        f2.write("\n#debug:  " + str(self.data.debugger.isDebug))


        for i in range(self.data.iterations.num_of_exper):
            if i != 0:
                self.createTableCA()


            # result-a
            f.write("\n\n\n#Experiment: " + str(i))
            f.write("\n\n#seed: " + str(self.automata.seed) + "")
            f.write("\n{0:10}{1:13}{2:18}{3:16}{4:16}{5:16}".format("#iter", "f_C", "f_C_corr", "av_sum", "f_allC", "f_allD"))
            f.write("{0:14}{1:14}{2:15}{3:20}{4:26}".format("f_kD", "f_kC", "f_kDC", "f_strat_ch", "f_strat_ch_final"))
            f.write("{0:17}{1:17}\n".format("f_cr_0s", "f_cr_1s"))

            # result-b
            f2.write("\n\n\n#Experiment: " + str(i))
            f2.write("\n\n#seed: " + str(self.automata.seed) + "")
            f2.write("\n{0:10}{1:14}{2:14}".format("iter", "f_0D", "f_1D"))
            f2.write("{0:14}{1:14}{2:14}{3:14}{4:14}{5:14}{6:14}".format("f_2D", "f_3D", "f_4D", "f_5D", "f_6D", "f_7D",
                                                                         "f_8D"))
            f2.write("{0:14}{1:14}{2:14}{3:14}{4:14}{5:14}{6:14}".format("f_0C", "f_1C", "f_2C", "f_3C", "f_4C", "f_5C",
                                                                         "f_6C"))
            f2.write("{0:14}{1:14}{2:15}{3:15}{4:15}{5:15}{6:15}".format("f_7C", "f_8C", "f_0DC", "f_1DC", "f_2DC", "f_3DC",
                                                                         "f_4DC"))
            f2.write("{0:15}{1:15}{2:15}{3:15}\n".format("f_5DC", "f_6DC", "f_7DC", "f_8DC"))

            stats_multirun_temp = []
            stats_multirun = []
            for statistics in self.automata.statistics:
                statistics.write_stats_to_file(f, f2)
                stats_multirun_temp.append(statistics)
            stats_multirun.append((i, stats_multirun_temp))

            if 0 < self.data.iterations.num_of_exper - 1 == i:
                statistics_multirun = StatisticsMultirun(stats_multirun, self.data.iterations.num_of_iter, self.data.iterations.num_of_exper)
                f3 = open("std-result-a.txt", "w")
                f3.write("#num_of_iter: " + str(self.data.iterations.num_of_iter))
                f3.write("\n#num_of_exper: " + str(self.data.iterations.num_of_exper))
                f3.write("\n#rows: " + str(self.data.canvas.rows))
                f3.write("\n#cols: " + str(self.data.canvas.cols))
                f3.write("\n#p_init_C: " + str(self.data.canvas.p_init_C))
                f3.write("\n#p_state_mut: " + str(self.data.mutations.p_state_mut))
                f3.write("\n#p_strat_mut: " + str(self.data.mutations.p_strat_mut))
                f3.write("\n#p_0_neighb: " + str(self.data.mutations.p_0_neighb_mut))
                f3.write("\n#p_1_neighb: " + str(self.data.mutations.p_1_neighb_mut))
                if (self.data.competition.isRoulette):
                    f3.write("\n#comp_type: roulette")
                elif (self.data.competition.isTournament):
                    f3.write("\n#comp_type: tournament")
                else:
                    f3.write("\n#comp_type: None?")

                f3.write("\n#sharing: " + str(self.data.canvas.isSharing))
                f3.write("\n#allC: " + str(self.data.strategies.all_C))
                f3.write("\n#allD: " + str(self.data.strategies.all_D))
                f3.write("\n#kD: " + str(self.data.strategies.k_D))
                f3.write("\n#kC: " + str(self.data.strategies.k_C))
                f3.write("\n#kDC: " + str(self.data.strategies.k_DC))
                f3.write("\n#k_values: " + str(self.data.strategies.k_var_min) + " to " + str(
                    self.data.strategies.k_var_max))
                f3.write("\n#synchronity_prob: " + str(self.data.synch.synch_prob))
                f3.write("\n#optimal_num_of_1s: " + str(self.data.synch.optimal_num_1s))
                f3.write("\n#playerC_opponentD_payoff: " + str(self.data.payoff.c))
                f3.write("\n#playerC_opponentC_payoff: " + str(self.data.payoff.d))
                f3.write("\n#playerD_opponentD_payoff: " + str(self.data.payoff.a))
                f3.write("\n#playerD_opponentC_payoff: " + str(self.data.payoff.b))
                f3.write("\n#debug:  " + str(self.data.debugger.isDebug))
                f3.write("\n\n{0:10}{1:16}{2:17}{3:20}{4:21}{5:19}".format("#iter", "av_f_C", "std_f_C", "av_f_C_corr", "std_f_C_corr",
                                                                           "av_av_pay"))
                f3.write("{0:20}{1:20}{2:21}{3:20}{4:21}".format("std_av_pay", "av_f_cr_0s", "std_f_cr_0s", "av_f_cr_1s", "std_f_cr_1s"))
                f3.write("{0:19}{1:20}{2:19}{3:20}{4:18}".format("av_f_allC", "std_f_allC", "av_f_allD", "std_f_allD",
                         "av_f_kD"))
                f3.write("{0:19}{1:18}{2:19}{3:19}{4:20}".format("std_f_kD", "av_f_kC", "std_f_kC", "av_f_kDC",
                         "std_f_kDC"))
                f3.write("{0:23}{1:24}{2:29}{3:30}\n".format("av_f_strat_ch", "std_f_strat_ch", "av_f_strat_ch_final", "std_f_strat_ch_final"))
                statistics_multirun.write_to_file(f3)

    # update display of CA depending on iteration
    # visualization mode defines what type of visualization is chosen (state/strategy)
    def change_iter_display(self):
        if self.visualization_mode == 0:
            self.state_color_handler()
        elif self.visualization_mode == 1:  # strategies
            self.strategies_color_handler()
        elif self.visualization_mode == 2:  # kD
            self.kD_strategies_color_handler()
        elif self.visualization_mode == 3:  # kC
            self.kC_strategies_color_handler()
        elif self.visualization_mode == 4:  # kDC
            self.kDC_strategies_color_handler()
        else:  # action
            self.action_color_handler()

    def enableStartButton(self):
        self.ui.pushButton_start.setEnabled(True) 

    def pause_animation(self):
        self.animation.stop()
        self.enableStartButton()

    # create a new seperate thread for simulation
    def start_animation_thread(self):
        if self.isAnimationRunning == True:
            self.animation.play()
        else:
            self.isAnimationRunning = True
            self.ui.disableStartButton()
            numOfIters = self.iterations.num_of_iter
            microSleepTime = 2 * self.data.canvas.rows * self.data.canvas.cols
            secSleepTime = microSleepTime / 10000
            self.animation = Animation(self, 0, numOfIters, secSleepTime)
            self.threadpool.start(self.animation)

    def start_animation(self):
        iter = self.ui.spinBox_iters.value()
        self.ui.spinBox_iters.setValue(iter + 1)
        #self.ui.graphicsView_CA.update()

