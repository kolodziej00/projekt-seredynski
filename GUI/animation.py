import time
from PySide6.QtCore import QRunnable

class Animation(QRunnable):
      def __init__(self, MainWindow, iter, numOfIters):
         super().__init__()
         self.mainWindow = MainWindow
         self.iter = iter
         self.numofIters = numOfIters
         self.isPaused = False
         self.isRunning = True

      def run(self):
         print("Running a new thread")
         while self.iter < self.numofIters - 1:
            if self.isPaused == True:
                time.sleep(0.1)
                continue
            self.mainWindow.start_animation()
            self.iter += 1
            time.sleep(0.3)
         self.mainWindow.enableStartButton()
         self.isRunning = False
         print("Thread done")

      def stop(self):
         self.isPaused = True

      def play(self):
          self.isPaused = False

      def stillRunning(self):
          return self.isRunning
      
      def terminate(self):
          self.iter = self.numofIters

