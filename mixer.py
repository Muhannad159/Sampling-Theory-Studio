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

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "mixer.ui"))  # connects the Ui file with the Python file


class MixerApp(QDialog, FORM_CLASS):  # go to the main window in the form_class file

    def __init__(self, parent=None):  # constructor to initiate the main window  in the design
        super(MixerApp, self).__init__(parent)
        self.setupUi(self)
        self.handle_btn()
        self.sin_time = np.linspace(0, 2, 1000) 
        self.sinusoidals = [] 
        self.sin_names = []
        self.sin_graphics_view.setBackground('w')

    def handle_btn(self):
          self.plot_push_btn.clicked.connect(self.construct_signal)

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
        self.max_freqs = self.max_frequencies = self.calculate_max_frequencies(self.sinusoidals, self.sample_rate)
        self.overall_max_frequency = max(self.max_freqs)

        self.sampled_signal = self.sample_signal(self.syntheticSignal, self.overall_max_frequency, self.sample_rate)
        if self.sampled_signal is not None:
        # Plot the sampled points as blue dots
            self.sin_graphics_view.plot(self.sin_time[::len(self.sin_time) // len(self.sampled_signal)],
                                    self.sampled_signal, pen=None, symbol='o', symbolPen=None, symbolBrush=(0, 0, 255))




    def calculate_max_frequency(self, synthetic_signal, sample_rate):
    # Step 1: Compute the Fourier Transform of the synthetic signal.
        fft_result = fft.fft(synthetic_signal)

    # Step 2: Find the frequency components in the FFT result.
        frequency_values = fft.fftfreq(len(fft_result), 1 / sample_rate)

    # Step 3: Identify the maximum frequency component.
        magnitudes = np.abs(fft_result)
        max_magnitude = np.max(magnitudes)
        max_frequency_index = np.argmax(magnitudes)
        max_frequency = frequency_values[max_frequency_index]

    # Step 4: Return the maximum frequency.
        return max_frequency

    def calculate_max_frequencies(self, sinusoidals, sample_rate):
        max_frequencies = []
        for sinusoidal in sinusoidals:
            max_freq = self.calculate_max_frequency(sinusoidal, sample_rate)
            max_frequencies.append(max_freq)
        return max_frequencies

        #print(F_max)
        # print(F_max)
        # self.fmax = int(F_max)
        # #print(self.fmax)
        # self.fs = 5 * self.fmax
        # #self.time_to_sample = 1/(self.fs)
        # self.sampled_time = (time)[::int(100 / self.fs)]
        # self.sampling_signal = (amplitude)[::int(100 / (self.fs))]
        # # self.time_to_sample=1/(self.sampling_signal)
        # self.sin_graphics_view.plot(
        #     self.sampled_time, self.sampling_signal, pen=None, symbol='o')

    def sample_signal(self, signal, max_frequency, sample_rate):
    # Calculate the Nyquist frequency based on the max frequency
        nyquist_frequency = max_frequency * 2

    # Calculate the number of samples per period based on the Nyquist frequency
        samples_per_period = int(sample_rate / nyquist_frequency)

    # Use NumPy to downsample the signal to the appropriate number of samples
        sampled_signal = signal[::samples_per_period]

        return sampled_signal

       



 

def main():  # method to start app
        app = QApplication(sys.argv)
        window = MixerApp()
        window.show()
        app.exec_()  # infinte Loop

if __name__ == '__main__':
        main()