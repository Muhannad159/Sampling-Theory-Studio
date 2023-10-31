# Import necessary libraries and modules
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from UliEngineering.SignalProcessing.Simulation import sine_wave  # Import custom signal processing module
import sys
from os import path
import numpy.fft as fft
import numpy as np
import pyqtgraph as pg
from main import MainApp  # Assuming there's a 'main' module for the main application

# Load the UI file for the mixer application
FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "mixer.ui"))

# Define the MixerApp class, a QDialog-based application for constructing and visualizing synthetic signals
class MixerApp(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Initialize the MixerApp.

        :param parent: The parent widget.
        """
        super(MixerApp, self).__init__(parent)
        # Initialize the UI
        self.setupUi(self)
        # Set up event handlers for buttons
        self.handle_btn()
        # Initialize time array for sine wave simulation
        self.sin_time = np.linspace(0, 3, 4000)
        # Store sine waves as a dictionary
        self.sinusoidals = {}
        self.sin_names = []
        # Set the background color of the graphics view
        self.sin_graphics_view.setBackground('w')
        # Set the x-axis label of the graphics view 
        self.sin_graphics_view.setLabel('bottom', 'time')

    def handle_btn(self):
        """
        Connect buttons to their respective functions.
        """
        self.plot_push_btn.clicked.connect(self.construct_signal)
        self.add_push_btn.clicked.connect(self.add_to_main)

    def add_to_main(self):
        """
        Add synthesized signals to the main application and update UI elements.
        """
        # Clear all existing signals in the main application
        self.mainapp.clear_all()

        # Populate a combo box in the main application with synthesized signals
        self.mainapp.refill_combo_from_dict(self.mainapp.comboBox_2, self.sinusoidals)

        # Calculate the sample rate and set frequency slider values
        self.mainapp.fs = 2 * self.overall_max_frequency
        self.mainapp.freq_slider.setRange(int(self.mainapp.fs / 8), int(self.mainapp.fs * 4))
        self.mainapp.freq_slider.setSliderPosition(int(2 * self.overall_max_frequency))
        self.mainapp.freq_slider.setValue(int(self.mainapp.fs))

        # Plot the synthetic signal in the main application
        self.mainapp.plot_graph()

    def set_myapp(self, mainapp):
        """
        Set the main application.

        :param mainapp: The main application instance.
        """
        self.mainapp = mainapp

    def construct_signal(self):
        """
        Create a synthetic signal based on user inputs.
        """
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

        # Validate magnitude and phase inputs as needed
        try:
            sin_magnitude = float(magnitude_input)
            sin_phase = float(phase_input)
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Magnitude and Phase must be valid numbers.')
            return

        # If no name is entered, construct a default name based on specs
        if not name_input:
            name_input = f"Freq_{sin_frequency}_Mag_{sin_magnitude}_Phase_{sin_phase}"

        # If the name already exists, generate a unique name
        suffix = 1
        base_name = name_input
        while name_input in self.sinusoidals:
            name_input = f"{base_name}_{suffix}"
            suffix += 1

        # Create the sine wave and add it to the dictionary
        self.sinusoidal = sine_wave(frequency=sin_frequency, samplerate=len(self.sin_time), amplitude=sin_magnitude,
                                    phaseshift=sin_phase)
        self.sinusoidals[name_input] = self.sinusoidal
        self.sin_names.append(name_input)

        # Draw and display the synthetic signal
        self.drawSyntheticSignal(self.sin_graphics_view)

    def sumSignals(self):
        """
        Calculate the synthetic signal by summing individual sine wave components.
        """
        if self.sinusoidals:
            self.syntheticSignal = np.zeros(len(self.sin_time))  # Initialize with zeros
            for name, sinusoidal in self.sinusoidals.items():
                self.syntheticSignal += sinusoidal  # Accumulate the sine waves
        else:
            self.syntheticSignal = None

    def drawSyntheticSignal(self, graphicsView):
        """
        Draw and display the synthetic signal on a graphics view.

        :param graphicsView: The graphics view to display the signal.
        """
        self.sumSignals()
        graphicsView.clear()

        # Plot the synthetic signal
        graphicsView.plot(self.sin_time, self.syntheticSignal, pen=pg.mkPen(color=(255, 0, 0)))

        # Calculate sample rate and maximum frequencies
        self.sample_rate = len(self.sin_time)
        self.max_freqs = self.calculate_max_frequencies(list(self.sinusoidals.values()), self.sample_rate)
        self.overall_max_frequency = max(self.max_freqs)

    def calculate_max_frequency(self, sinusoidal, sample_rate):
        """
        Calculate the maximum frequency of a sine wave component using FFT.

        :param sinusoidal: The input sine wave.
        :param sample_rate: The sample rate.
        :return: The maximum frequency.
        """
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
        """
        Calculate the maximum frequencies for all sine wave components.

        :param sinusoidals: A list of sine wave components.
        :param sample_rate: The sample rate.
        :return: A list of maximum frequencies.
        """
        max_frequencies = []
        for sinusoidal in sinusoidals:
            max_freq = self.calculate_max_frequency(sinusoidal, sample_rate)
            max_frequencies.append(max_freq)
        return max_frequencies
 

def main():  # method to start app
        app = QApplication(sys.argv)
        window = MixerApp()
        window.show()
        app.exec_()  # infinte Loop

if __name__ == '__main__':
        main()