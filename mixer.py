from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from UliEngineering.SignalProcessing.Simulation import sine_wave
import os
import sys
from os import path
import numpy as np

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "mixer.ui"))  # connects the Ui file with the Python file


class MainApp(QDialog, FORM_CLASS):  # go to the main window in the form_class file

    def __init__(self, parent=None):  # constructor to initiate the main window  in the design
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.handle_btn()
        self.sin_time = np.linspace(0, 2, 1000) 
        self.sinusoidals = [] 

    def handle_btn(self):
          self.add_push_btn.clicked.connect(self.construct_signal)

    def construct_signal(self):
        self.sin_frequency = float(self.signalFrequency.text())
        self.sin_magnitude = float(self.signalMagnitude.text())
        self.sin_phase = float(self.signalPhase.text())
        self.sinusoidal = sine_wave(frequency=self.sin_frequency, samplerate=len(
         self.sin_time), amplitude=self.sin_magnitude, phaseshift=self.sin_phase)
        self.add_sinusoidal(self.sinusoidal)
        self.sin_graphics_view.clear()
        self.sin_graphics_view.plot(self.sin_time, self.sinusoidal, pen=pg.mkPen(color=(255, 0, 0)))
        print(self.sin_frequency)

    

def main():  # method to start app
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()  # infinte Loop

if __name__ == '__main__':
        main()