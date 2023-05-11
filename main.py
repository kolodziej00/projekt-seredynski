# This Python file uses the following encoding: utf-8

import sys

from PySide6.QtWidgets import QApplication

from GUI.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

