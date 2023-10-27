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


class MixerApp(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        super(MixerApp, self).__init__(parent)

        self.setupUi(self)
        self.handle_btn()
        self.sin_time = np.linspace(0, 1, 1000)
        self.sinusoidals = {}  # Store sine waves as a dictionary
        self.sin_names = []
        self.sin_graphics_view.setBackground('w')

    def handle_btn(self):
        self.plot_push_btn.clicked.connect(self.construct_signal)
        self.add_push_btn.clicked.connect(self.add_to_main)

    def add_to_main(self):
        self.mainapp.clear_all()
        self.mainapp.refill_combo_from_dict(self.mainapp.comboBox_2, self.sinusoidals)
        self.mainapp.plot_graph()

    def set_myapp(self, mainapp):
        self.mainapp = mainapp

    def construct_signal(self):
        # Get input values from QLineEdit widgets
        freq_input = self.signalFrequency.text()
        magnitude_input = self.signalMagnitude.text()
        phase_input = self.signalPhase.text()
        name_input = self.signalName.text()

        # Validate the frequency input
        try:
            sin_frequency = float(freq_input)
            if sin_frequency <= 0:
                QMessageBox.warning(self, 'Invalid Input', 'Frequency must be a positive number.')
                return
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Frequency must be a valid number.')
            return

        # Validate the name input
        if name_input in self.sinusoidals:
            QMessageBox.warning(self, 'Invalid Input', 'Name already exists. Please choose a different name.')
            return

        # Validate magnitude and phase inputs as needed
        try:
            sin_magnitude = float(magnitude_input)
            sin_phase = float(phase_input)
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Magnitude and Phase must be valid numbers.')
            return

        # If all validations pass, create the sine wave and add it to the dictionary
        self.sinusoidal = sine_wave(frequency=sin_frequency, samplerate=len(self.sin_time), amplitude=sin_magnitude,
                                    phaseshift=sin_phase)
        self.sinusoidals[name_input] = self.sinusoidal
        self.sin_names.append(name_input)
        self.drawSyntheticSignal()

    def sumSignals(self):
        if self.sinusoidals:
            self.syntheticSignal = np.zeros(len(self.sin_time))  # Initialize with zeros
            for name, sinusoidal in self.sinusoidals.items():
                self.syntheticSignal += sinusoidal  # Accumulate the sine waves
        else:
            self.syntheticSignal = None

    def drawSyntheticSignal(self):
        self.sumSignals()
        self.sin_graphics_view.clear()
        self.sin_graphics_view.plot(self.sin_time, self.syntheticSignal, pen=pg.mkPen(color=(255, 0, 0)))
        self.sample_rate = len(self.sin_time)
        self.max_freqs = self.calculate_max_frequencies(list(self.sinusoidals.values()), self.sample_rate)
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