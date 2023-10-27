from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from UliEngineering.SignalProcessing.Simulation import sine_wave
import os
import sys
from os import path
import numpy.fft as fft
import numpy as np
import pyqtgraph as pg
from main import MainApp
FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "mixer.ui"))  # connects the Ui file with the Python file


class MixerApp(QDialog, FORM_CLASS):  # go to the main window in the form_class file

    def __init__(self, parent=None ):  # constructor to initiate the main window  in the design
        super(MixerApp, self).__init__(parent)
        
        self.setupUi(self)
        self.handle_btn()
        self.sin_time = np.linspace(0, 1, 1000) 
        self.sinusoidals = [] 
        self.sin_names = []
        self.sin_graphics_view.setBackground('w')
        
        
    def handle_btn(self):
          self.plot_push_btn.clicked.connect(self.construct_signal)
          self.add_push_btn.clicked.connect(self.add_to_main)


    def add_to_main(self):
        #print("hello")
        self.mainapp.graphicsView.clear()
        self.mainapp.graphicsView_2.clear()
        self.mainapp.graphicsView_3.clear()
        self.mainapp.plot_graph()  
        
        
     
    def set_myapp(self , mainapp):
        self.mainapp = mainapp
         

    def construct_signal(self):
        self.sin_frequency = float(self.signalFrequency.text())
        self.sin_magnitude = float(self.signalMagnitude.text())
        self.sin_phase = float(self.signalPhase.text())
        self.sin_name = self.signalName.text()
        self.sinusoidal = sine_wave(frequency=self.sin_frequency, samplerate=len(
            self.sin_time), amplitude=self.sin_magnitude, phaseshift=self.sin_phase)
        self.sinusoidals.append(self.sinusoidal)
        self.sin_names.append(self.sin_name)
        self.drawSyntheticSignal()
        self.lcdNumber.display(self.overall_max_frequency)

    def drawSyntheticSignal(self):
        self.syntheticSignal = [0]*self.sin_time
        for sinusoidal in self.sinusoidals:
            self.syntheticSignal += sinusoidal
        self.sin_graphics_view.clear()
        self.sin_graphics_view.plot(self.sin_time, self.syntheticSignal, pen=pg.mkPen(color=(255, 0, 0)))
        self.sample_rate = len(self.sin_time) 
        self.max_freqs = self.calculate_max_frequencies(self.sinusoidals, self.sample_rate)
        self.overall_max_frequency = max(self.max_freqs)
    #     print(self.overall_max_frequency)
    #     self.sampled_signal = self.sample_signal(self.syntheticSignal, self.overall_max_frequency, self.sample_rate)
    #     if self.sampled_signal is not None:
    # # Plot the sampled points as blue dots
    #         self.sin_graphics_view.plot(self.sin_time[::len(self.sin_time) // len(self.sampled_signal)],
    #                            self.sampled_signal, pen=None, symbol='o', symbolPen=None, symbolBrush=(0, 0, 255))





    def calculate_max_frequency(self, sinusoidal, sample_rate):
    # Step 1: Compute the Fourier Transform of the individual sinusoidal component.
        fft_result = fft.fft(sinusoidal)

        # Step 2: Find the frequency components in the FFT result.
        frequency_values = fft.fftfreq(len(fft_result), 1 / sample_rate)

        # Step 3: Identify the maximum magnitude and its corresponding frequency index.
        magnitudes = np.abs(fft_result)
        max_magnitude = np.max(magnitudes)
        max_magnitude_index = np.argmax(magnitudes)

        # Step 4: Find the corresponding frequency for the maximum magnitude.
        max_frequency = frequency_values[max_magnitude_index]

        # Step 5: Ensure the frequency is positive or zero.
        if max_frequency < 0:
            max_frequency = -max_frequency

        # Step 6: Return the maximum frequency.
        return max_frequency



    def calculate_max_frequencies(self, sinusoidals, sample_rate):
        max_frequencies = []
        for sinusoidal in sinusoidals:
            max_freq = self.calculate_max_frequency(sinusoidal, sample_rate)
            max_frequencies.append(max_freq)
        return max_frequencies


    # def sample_signal(self, signal, max_frequency, sample_rate):
    #     # Calculate the Nyquist frequency based on the max frequency
    #     nyquist_frequency = max_frequency * 2

    #     # Calculate the number of samples per period based on the Nyquist frequency
    #     samples_per_period = int(sample_rate / nyquist_frequency)

    #     # Determine the number of periods in the signal
    #     num_periods = len(signal) // samples_per_period

    #     # Calculate the step size for sampling
    #     step_size = len(signal) // num_periods

    #     # Sample the signal at the determined step size
    #     sampled_signal = signal[::step_size]

    #     return sampled_signal




       



 

def main():  # method to start app
        app = QApplication(sys.argv)
        window = MixerApp()
        window.show()
        app.exec_()  # infinte Loop

if __name__ == '__main__':
        main()