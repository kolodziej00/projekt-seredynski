import asyncio
import time
from PySide6.QtCore import QRunnable, QMutex

class Animation(QRunnable):

      def __init__(self, MainWindow, iter, numOfIters, sleepTime):
         super().__init__()
         self.mainWindow = MainWindow
         self.iter = iter
         self.numofIters = numOfIters
         if sleepTime > 0.3:
            self.sleepTime = 0.3
            self.extendedSleepTime = 1.3 * sleepTime
         else:
             self.sleepTime = 0.1
             self.extendedSleepTime = 0.4
         self.isPaused = False
         self.isRunning = True
         self.mutex = QMutex()


      def run(self):
         print("Running a new thread")
         while self.iter < self.numofIters - 1:
            if self.isPaused == True:
                time.sleep(0.1)
                continue
            self.mutex.lock()
            self.mainWindow.start_animation()
            self.mutex.unlock()
            self.iter += 1
            time.sleep(self.sleepTime)
         self.mainWindow.enableStartButton()
         self.isRunning = False
         print("Thread done")
         self.mainWindow.isAnimationRunning = False
         #self.mutex.endPaint()

      def extendSleepTime(self):
          self.sleepTime = self.extendedSleepTime

      def stop(self):
         self.isPaused = True

      def play(self):
          self.isPaused = False

      def stillRunning(self):
          return self.isRunning
      
      def terminate(self):
          self.iter = self.numofIters

