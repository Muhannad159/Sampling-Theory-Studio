from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QFileDialog
from mixer import MixerApp
import pandas as pd
import pyqtgraph as pg
import random  # Import the random module to add noise
import os
import sys
import numpy as np
from os import path

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
        self.handle_btn()
        self.fs = 100
        
    
    def handle_btn(self):
        self.actionOpen_file.triggered.connect(self.add_signal)
        self.mix_signal_btn.triggered.connect(self.open_mixer)
        self.noise_slider.valueChanged.connect(self.update_noise_level)
        self.delete_btn.clicked.connect(self.delete_signal)  # Connect the delete button here
        self.freq_slider.valueChanged.connect(self.update_fs)



    def delete_signal(self):
        if not self.signals_data:
            return  # No items in the dictionary to delete

        selected_item_text = self.comboBox_2.currentText()  # Get the currently selected item text
        selected_signal_index = int(selected_item_text.split('-')[-1].strip())  # Extract the signal index
        self.count_signals -= 1

        if selected_signal_index in self.signals_data:
            del self.signals_data[selected_signal_index]

        self.comboBox_2.removeItem(self.comboBox_2.currentIndex())  # Remove the selected item from the combobox
        self.way_of_plotting_with_add = True
        self.plot_graph()  # Update the plot immediately after deletion

    def open_mixer(self):
        self.mixer = MixerApp()
        self.mixer.show()
 
                        
    def plot_graph(self):
        self.graphicsView.clear()
        if self.way_of_plotting_with_add:
            for value in self.signals_data.values():
                pen = pg.mkPen(color=(255, 0, 0))
                x = value[0]
                y = value[1]
                
                # Apply noise to 'y' values
                noisy_y = [v + random.uniform(-self.noise_level, self.noise_level) for v in y]
                
                # Set the sampling rate
                # Adjust the sampling rate as needed
                
                
                # Sample the continuous signal
                #sampled_x = np.linspace(0, max(x), len(x), endpoint=False)
                sampled_x = np.linspace(0, max(x), self.fs, endpoint=False)
                #print(sampled_x)
                sampled_y = [y[np.argmin(np.abs(x - x_sample))] for x_sample in sampled_x]
                
                # Plot the noisy signal
                data_line = self.graphicsView.plot(x, noisy_y, pen=pen)
                
                # Plot the sampled points
                sampled_points = self.graphicsView.plot(sampled_x, sampled_y, pen=None, symbol='o', symbolBrush='b')
                
                # Perform reconstruction (original signal, not sampled)
                reconstructed_signal = np.zeros_like(x)
                for n, sample in enumerate(sampled_y):
                    reconstructed_signal += sample * np.sinc((x - sampled_x[n]) / (1 / self.fs))
                    #print(reconstructed_signal)
                
                # Plot the reconstructed signal
                reconstruction_pen = pg.mkPen(color=(0, 0, 255))
                self.graphicsView_2.plot(x, reconstructed_signal, pen=reconstruction_pen)

   

            
    
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
            time_column = signal_data.iloc[:, 0]
            values_column = signal_data.iloc[:, 1]
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


    def update_noise_level(self, value):
        self.noise_level = value / 100
        self.plot_graph()

    def update_fs(self,value ):
         self.fs = value*10
         self.graphicsView_2.clear()
         self.plot_graph()
        
def main():  # method to start app
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()  # infinte Loop

if __name__ == '__main__':
     main()
