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
        

# TODO: Handle many iterations
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
        fileName = "Images//image" + str(self.ui.lcdNumber_iters.value()) + ".png"
        pixmap.save(fileName, "PNG", -1)

    def changeCellsColor(self, selected, R, G, B, opacity=255):
        for ix in selected:
            row, column = ix
            self.ui.graphicsView_CA.item(row, column).setBackground(QColor(R,G,B, opacity))
                
                
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
        self.automata = CA(rows, cols, self.data.canvas.p_init_C, self.data.strategies.all_C,
                       self.data.strategies.all_D, self.data.strategies.k_D, self.data.strategies.k_C,
                       self.data.strategies.k_var_min, self.data.strategies.k_var_max, self.data.iterations.num_of_iter,
                       self.data.payoff.d, self.data.payoff.c, self.data.payoff.b, self.data.payoff.a, self.canvas.isSharing,
                       self.data.synch.synch_prob, self.data.competition.isTournament, self.data.mutations.p_state_mut,
                       self.data.mutations.p_strat_mut, self.data.mutations.p_0_neighb_mut, self.data.mutations.p_1_neighb_mut,
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
        selected = []
        iter = self.ui.spinBox_iters.value()
        k, cells = self.automata.cells[iter]
        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(255, 255, 255, 255))
                if cells[i, j].state == 1:
                    selected.append((i, j))
        self.changeCellsColor(selected, 255, 100, 0)
        self.visualization_mode = 0
        
        
    def strategies_color_handler(self):
        if self.isAnimationRunning == True:
            self.animation.extendSleepTime()
            
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        selected_all_C = []
        selected_all_D = []
        selected_kD = []
        selected_kC = []
        selected_kDC = []
        iter = self.ui.spinBox_iters.value()
        k, cells = self.automata.cells[iter]
        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(255, 255, 255, 255))
                # all D
                if cells[i, j].strategy == 0:
                    selected_all_D.append((i, j))
                # all C
                elif cells[i, j].strategy == 1:
                    selected_all_C.append((i, j))
                # kD
                elif cells[i, j].strategy == 2:
                    selected_kD.append((i, j))
                # kC
                elif cells[i, j].strategy == 3:
                    selected_kC.append((i, j))
                # kDC
                elif cells[i, j].strategy == 4:
                    selected_kDC.append((i, j))
        
        self.changeCellsColor(selected_all_C, 255, 100, 0) # red
        self.changeCellsColor(selected_all_D, 0, 0, 255) # blue
        self.changeCellsColor(selected_kD, 0, 128, 0) # green
        self.changeCellsColor(selected_kC, 0, 255, 255) # cyan
        self.changeCellsColor(selected_kDC, 255, 20, 147) # pink
        self.visualization_mode = 1

    def kD_strategies_color_handler(self):
        if self.isAnimationRunning == True:
            self.animation.extendSleepTime()

        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        selected_k_0 = []
        selected_k_1 = []
        selected_k_2 = []
        selected_k_3 = []
        selected_k_4 = []
        selected_k_5 = []
        selected_k_6 = []
        selected_k_7 = []
        selected_k_8 = []
        iter = self.ui.spinBox_iters.value()
        k, cells = self.automata.cells[iter]
        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(0, 0, 0, 255))
                if cells[i, j].strategy == 2:
                    if cells[i, j].k == 0:
                        selected_k_0.append((i, j))
                    elif cells[i, j].k == 1:
                        selected_k_1.append((i, j))
                    elif cells[i, j].k == 2:
                        selected_k_2.append((i, j))
                    elif cells[i, j].k == 3:
                        selected_k_3.append((i, j))
                    elif cells[i, j].k == 4:
                        selected_k_4.append((i, j))
                    elif cells[i, j].k == 5:
                        selected_k_5.append((i, j))
                    elif cells[i, j].k == 6:
                        selected_k_6.append((i, j))
                    elif cells[i, j].k == 7:
                        selected_k_7.append((i, j))
                    elif cells[i, j].k == 8:
                        selected_k_8.append((i, j))


        self.changeCellsColor(selected_k_0, 0, 128, 0, 0)
        self.changeCellsColor(selected_k_1, 0, 128, 0, 31)
        self.changeCellsColor(selected_k_2, 0, 128, 0, 62)
        self.changeCellsColor(selected_k_3, 0, 128, 0, 93)
        self.changeCellsColor(selected_k_4, 0, 128, 0, 124)
        self.changeCellsColor(selected_k_5, 0, 128, 0, 156)
        self.changeCellsColor(selected_k_6, 0, 128, 0, 187)
        self.changeCellsColor(selected_k_7, 0, 128, 0, 218)
        self.changeCellsColor(selected_k_8, 0, 128, 0, 255)

        self.visualization_mode = 2

    def kC_strategies_color_handler(self):
        if self.isAnimationRunning == True:
            self.animation.extendSleepTime()
        
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        selected_k_0 = []
        selected_k_1 = []
        selected_k_2 = []
        selected_k_3 = []
        selected_k_4 = []
        selected_k_5 = []
        selected_k_6 = []
        selected_k_7 = []
        selected_k_8 = []
        iter = self.ui.spinBox_iters.value()
        k, cells = self.automata.cells[iter]
        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(0, 0, 0, 200))
                if cells[i, j].strategy == 3:
                    if cells[i, j].k == 0:
                        selected_k_0.append((i, j))
                    elif cells[i, j].k == 1:
                        selected_k_1.append((i, j))
                    elif cells[i, j].k == 2:
                        selected_k_2.append((i, j))
                    elif cells[i, j].k == 3:
                        selected_k_3.append((i, j))
                    elif cells[i, j].k == 4:
                        selected_k_4.append((i, j))
                    elif cells[i, j].k == 5:
                        selected_k_5.append((i, j))
                    elif cells[i, j].k == 6:
                        selected_k_6.append((i, j))
                    elif cells[i, j].k == 7:
                        selected_k_7.append((i, j))
                    elif cells[i, j].k == 8:
                        selected_k_8.append((i, j))

        self.changeCellsColor(selected_k_0, 0, 255, 255, 0)
        self.changeCellsColor(selected_k_1, 0, 255, 255, 31)
        self.changeCellsColor(selected_k_2, 0, 255, 255, 62)
        self.changeCellsColor(selected_k_3, 0, 255, 255, 93)
        self.changeCellsColor(selected_k_4, 0, 255, 255, 124)
        self.changeCellsColor(selected_k_5, 0, 255, 255, 156)
        self.changeCellsColor(selected_k_6, 0, 255, 255, 187)
        self.changeCellsColor(selected_k_7, 0, 255, 255, 218)
        self.changeCellsColor(selected_k_8, 0, 255, 255, 255)

        self.visualization_mode = 3

    def kDC_strategies_color_handler(self):
        if self.isAnimationRunning == True:
            self.animation.extendSleepTime()

        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        selected_k_0 = []
        selected_k_1 = []
        selected_k_2 = []
        selected_k_3 = []
        selected_k_4 = []
        selected_k_5 = []
        selected_k_6 = []
        selected_k_7 = []
        selected_k_8 = []
        iter = self.ui.spinBox_iters.value()
        k, cells = self.automata.cells[iter]
        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(0, 0, 0, 200))
                if cells[i, j].strategy == 4:
                    if cells[i, j].k == 0:
                        selected_k_0.append((i, j))
                    elif cells[i, j].k == 1:
                        selected_k_1.append((i, j))
                    elif cells[i, j].k == 2:
                        selected_k_2.append((i, j))
                    elif cells[i, j].k == 3:
                        selected_k_3.append((i, j))
                    elif cells[i, j].k == 4:
                        selected_k_4.append((i, j))
                    elif cells[i, j].k == 5:
                        selected_k_5.append((i, j))
                    elif cells[i, j].k == 6:
                        selected_k_6.append((i, j))
                    elif cells[i, j].k == 7:
                        selected_k_7.append((i, j))
                    elif cells[i, j].k == 8:
                        selected_k_8.append((i, j))

        self.changeCellsColor(selected_k_0, 255, 20, 147, 0)
        self.changeCellsColor(selected_k_1, 255, 20, 147, 31)
        self.changeCellsColor(selected_k_2, 255, 20, 147, 62)
        self.changeCellsColor(selected_k_3, 255, 20, 147, 93)
        self.changeCellsColor(selected_k_4, 255, 20, 147, 124)
        self.changeCellsColor(selected_k_5, 255, 20, 147, 156)
        self.changeCellsColor(selected_k_6, 255, 20, 147, 187)
        self.changeCellsColor(selected_k_7, 255, 20, 147, 218)
        self.changeCellsColor(selected_k_8, 255, 20, 147, 255)

        self.visualization_mode = 4

    def action_color_handler(self):
        rows = self.data.canvas.rows
        cols = self.data.canvas.cols
        selected = []
        iter = self.ui.spinBox_iters.value()
        k, cells = self.automata.cells[iter]

        for i in range(rows):
            for j in range(cols):
                self.ui.graphicsView_CA.item(i, j).setBackground(QColor(0, 0, 255, 255))
                if cells[i, j].action == 1:
                    selected.append((i, j))
        self.changeCellsColor(selected, 255, 100, 0)
        self.visualization_mode = 5
        


    def save_results(self):
        f = open("result.txt", "w")
        f.write("#num_of_iter: " + str(self.data.iterations.num_of_iter))
        f.write("\n#num_of_exper: 1" + str(self.data.iterations.num_of_exper))
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
        elif():
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

        for i in range(self.data.iterations.num_of_exper):
            if i != 0:
                self.createTableCA()
            f.write("\n\n\n#Experiment: " + str(i))
            f.write("\n\n#seed: " + str(self.automata.seed) + "")
            f.write("\n#iter         f_C          f_C_corr        av_sum      f_allC      f_allD")
            f.write("        f_kD        f_kC        f_kDC       f_strat_ch      f_0D        f_1D")
            f.write("        f_2D        f_3D        f_4D        f_5D        f_6D        f_7D        f_8D")
            f.write("        f_0C        f_1C        f_2C        f_3C        f_4C        f_5C        f_6C")
            f.write("        f_7C        f_8C        f_0DC       f_1DC       f_2DC       f_3DC       f_4DC")
            f.write("        f_5DC       f_6DC       f_7DC       f_8DC\n")
            for statistics in self.automata.statistics:
                statistics.write_stats_to_file(f)


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

    # animation starts here
    def start_animation(self):
        iter = self.ui.spinBox_iters.value()
        self.ui.spinBox_iters.setValue(iter + 1)
        self.ui.graphicsView_CA.repaint()
        
