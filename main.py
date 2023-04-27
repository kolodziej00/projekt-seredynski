# This Python file uses the following encoding: utf-8

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject

from GUI.mainwindow import MainWindow
from algorithm.CA import CA

def main():
    # ca = CA(10, 10, 0.5, 0.2, 0.2, 0.2, 0.2, 0, 8)
    # z=0
    # for i in range(0, 10):
    #     for j in range(0,10):
    #         print(str(z) + ":")
    #         print("Cell state: " + str( ca.cells[i,j].state) )
    #         print("Cell strategy: " + str( ca.cells[i,j].strategy))
    #         z = z + 1
    #         print("Cell k: " + str( ca.cells[i,j].k) + "\n")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

