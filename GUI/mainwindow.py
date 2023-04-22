# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 10:35:46 2023

@author: pozdro
"""


from PySide6.QtWidgets import QMainWindow
from GUI.ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            

            
