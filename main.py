from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QFileDialog

import pandas as pd
import pyqtgraph as pg
import random  # Import the random module to add noise
import os
import sys
import numpy as np
from os import path
import scipy.signal
from scipy.interpolate import interp1d

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))  # connects the Ui file with the Python file


class MainApp(QMainWindow, FORM_CLASS):  # go to the main window in the form_class file

    def __init__(self, parent=None):  # constructor to initiate the main window  in the design
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.graphicsView.setBackground('w')
        self.graphicsView_2.setBackground('w')
        self.graphicsView_3.setBackground('w')
        self.signals_data = {}  # Define signals_data as a class attribute
        self.count_signals = 0
        self.file_names= []
        self.noise_slider.setOrientation(Qt.Horizontal)
        self.noise_slider.setRange(0, 100)  # Set the range of the noise level as per your requirements
        self.noise_level = 0  # Initialize the noise level
        self.way_of_plotting_with_add = False
        self.handle_btn()
        self.fs = 125
               

    def handle_btn(self):
        self.actionOpen_file.triggered.connect(self.add_signal)
        self.mix_signal_btn.triggered.connect(self.open_mixer)
        self.noise_slider.valueChanged.connect(self.update_noise_level)
        self.delete_btn.clicked.connect(self.delete_signal)  # Connect the delete button here
        self.freq_slider.valueChanged.connect(self.update_fs)
        
        
        
    
    def reindex_dict_keys(self, dictionary):
        return {i: value for i, (key, value) in enumerate(dictionary.items(), start=1)}

    # A function to refill the comboBox
    def refill_combo_from_dict(self, combo_box, dictionary):
        combo_box.clear()  # Clear the combo box
        combo_box.addItem("Select a Signal")
        # Add items from the dictionary to the combo box
        for key in dictionary:
            combo_box.addItem(f"{'Signal'} - {key}")

    def delete_signal(self):
        if self.way_of_plotting_with_add:
            selected_item_text = self.comboBox_2.currentText()  # Get the currently selected item text
            selected_signal_index = int(selected_item_text.split('-')[-1].strip())  # Extract the signal index

            if selected_signal_index in self.signals_data:
                del self.signals_data[selected_signal_index]

                # Remove the selected item from the comboBox_2
                self.comboBox_2.removeItem(self.comboBox_2.currentIndex())

                # Clear all three graphics views
                self.clear_all()

                # Reorder the items in comboBox_2
                self.signals_data = self.reindex_dict_keys(self.signals_data)
                self.refill_combo_from_dict(self.comboBox_2, self.signals_data)

            # Replot the remaining signals
            self.plot_graph()

    def open_mixer(self):
        self.way_of_plotting_with_add = False
        from mixer import MixerApp
        self.mixer = MixerApp()
        self.mixer.set_myapp(self )
        self.mixer.show()


    def printt(self):
        print("hello")
    def plot_graph(self):
        self.graphicsView.clear()
        if self.way_of_plotting_with_add:
            #fmax = 0.5 * f_sample
            for value in self.signals_data.values():
                pen = pg.mkPen(color=(255, 0, 0))
                x = value[0]
                y = value[1]
                # Apply noise to 'y' values
                noisy_y = [v + random.uniform(-self.noise_level, self.noise_level) for v in y]
                # Set the sampling rate

                f_sample = 125
                time_interval = 1 / f_sample
                sampled_x, sampled_y = self.sample_signal(x, noisy_y, f_sample)
                reconstructed_signal = np.zeros(len(x))
                for i, t in enumerate(x):
                    reconstructed_signal[i] = np.sum(sampled_y * np.sinc((t - sampled_x) / time_interval))

                self.graphicsView.plot(sampled_x, sampled_y, pen="r", symbol='o', symbolBrush='b')
                reconstruction_pen = pg.mkPen(color=(0, 0, 255))
                self.graphicsView_2.plot(x, reconstructed_signal, pen=reconstruction_pen)
                error = [abs(original - reconstructed) for original, reconstructed in
                         zip(noisy_y, reconstructed_signal)]

                # Plot the error
                error_pen = pg.mkPen(color="r")
                self.graphicsView_3.plot(x, error, pen=error_pen)
        else:
            # # Apply noise to 'y' values
            # noisy_y = [v + random.uniform(-self.noise_level, self.noise_level) for v in self.mixer.syntheticSignal]
            # self.graphicsView.plot(self.mixer.sin_time, noisy_y, pen=pg.mkPen(color=(255, 0, 0)))
            # fm = self.mixer.overall_max_frequency
            # sampled_x, sampled_y = self.sample_signal(self.mixer.sin_time, noisy_y, 2*fm)
            # self.graphicsView.plot(sampled_x, sampled_y, pen=None,  symbol='o', symbolBrush='b')
            # reconstructed_signal = np.zeros(len(self.mixer.sin_time))
            # time_interval = 1 / (2*fm)
            # for i, t in enumerate(self.mixer.sin_time):
            #     reconstructed_signal[i] = np.sum(sampled_y * np.sinc((t - sampled_x) / time_interval))
            # reconstruction_pen = pg.mkPen(color=(0, 0, 255))
            # self.graphicsView_2.plot(self.mixer.sin_time, reconstructed_signal, pen=pg.mkPen(color=(255, 0, 0)))
            # #self.graphicsView_2.plot(sampled_x, sampled_y, pen=None,  symbol='o', symbolBrush='b')
            # print(fm)

            # Apply noise to 'y' values
            noisy_y = [v + random.uniform(-self.noise_level, self.noise_level) for v in self.mixer.syntheticSignal]
            self.graphicsView.plot(self.mixer.sin_time, noisy_y, pen=pg.mkPen(color=(255, 0, 0)))

            fm = self.mixer.overall_max_frequency
            sampled_x, sampled_y = self.sample_signal(self.mixer.sin_time, noisy_y, 2 * fm)
            self.graphicsView.plot(sampled_x, sampled_y, pen=None, symbol='o', symbolBrush='b')
            reconstructed_signal = self.interpolation_function(self.mixer.sin_time, noisy_y)  # Use the modified function here
            reconstruction_pen = pg.mkPen(color=(255, 0, 0))
            self.graphicsView_2.plot(self.mixer.sin_time, reconstructed_signal, pen=reconstruction_pen)
            print(fm)
            # error
            error = [abs(original - reconstructed) for original, reconstructed in
                     zip(noisy_y, reconstructed_signal)]
            # Plot the error
            error_pen = pg.mkPen(color="r")
            self.graphicsView_3.plot(self.mixer.sin_time, error, pen=error_pen)
            print(fm)

    def sample_signal(self,original_x, original_y, f_sample):
        # Calculate the time interval between samples
        time_interval = 1 / f_sample
        
        # Create a new array of sample times based on the time interval
        new_sample_times = np.arange(0, max(original_x), time_interval)
        
        # Initialize an array for the sampled signal
        sampled_signal = np.zeros(len(new_sample_times))
        
        # Sample the signal at the specified times
        for i, t in enumerate(new_sample_times):
            # Find the closest original sample to the current time
            closest_sample_idx = np.argmin(np.abs(original_x - t))
            sampled_signal[i] = original_y[closest_sample_idx]
        
        return new_sample_times, sampled_signal

    def interpolation_function(self, x, y):
        # Clip the values to the range [0, 0.75]
        x_new = np.clip(x, 0, 200)

        # Create an interpolator using sinc interpolation
        interpolator = interp1d(self.mixer.sin_time, y, kind='cubic')

        # Interpolate the values
        y = interpolator(x_new)

        return y

    def add_signal(self):
         options  = QFileDialog().options()
         options |= QFileDialog.ReadOnly
         file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                   options=options)
         if file_path:
            self.count_signals += 1
            file_name = file_path.split("/")[-1]
            self.file_names.append(file_name)
            signal_data = pd.read_csv(file_name)
            time_column = signal_data.iloc[:1000, 0]
            values_column = signal_data.iloc[:1000, -1]
            time_values = time_column.tolist()
            v_values = values_column.tolist()
            self.first_element_of_time = time_values[1]-time_values[0]
            self.max_x_1 = max(time_values)
            self.number_of_points = len(time_values)

            # Making a new item in the dictionary, the new signal is given a key, and the values is given according to its data
            self.signals_data[self.count_signals] = [time_values, v_values, 'Red', f"{'Signal'} - {self.count_signals}", file_name]
            self.comboBox_2.addItem(f"{'Signal'} - {self.count_signals}")
            self.way_of_plotting_with_add = True
         self.plot_graph()

    def clear_all(self):
        self.graphicsView.clear()
        self.graphicsView_2.clear()
        self.graphicsView_3.clear()

    def update_noise_level(self, value):
        self.clear_all()
        self.noise_level = value / 100
        self.nsr_lbl.setText(f"Noise to Signal Ratio {str(self.noise_level)}")
        self.plot_graph()

    def update_fs(self,value):
         self.fs = value*10
         self.freq_lbl.setText(f"Sampling frequency is {str(self.fs)}")
         self.clear_all()
         self.plot_graph()

def main():  # method to start app
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()  # infinte Loop

if __name__ == '__main__':
     main()
