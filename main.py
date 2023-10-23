from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QFileDialog
from mixer import MixerApp
import pandas as pd
import pyqtgraph as pg
import os
import sys
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
        self.handle_btn()
    
    def handle_btn(self):
        self.actionOpen_file.triggered.connect(self.add_signal)
        self.mix_signal_btn.triggered.connect(self.open_mixer)
    def open_mixer(self):
        self.mixer = MixerApp()
        self.mixer.show()
    
    
    
    def plot_graph(self):
        if self.way_of_plotting_with_add : 
        #self.color_detect(self.signals_data)
        #self.graphicsView_1.setObjectName("graphicsView_1")
    
        
        #self.graphicsView_1.setXRange(0, 616 * self.first_element_of_time)
            for value in self.signals_data.values():
                
                pen = pg.mkPen(color=(255 , 0 , 0))
                x = value[0]
                y = value[1]
                data_line = self.graphicsView.plot(x, y, pen=pen)
                data_line.x_data = x
                data_line.y_data = y
        
        if not self.signals_data:
            return
        
        #self.max_range_1()
        #self.graphicsView_1.setYRange(-self.max_y_1, self.max_y_1)
        
    
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
        
        # Update the table with the latest data
        




def main():  # method to start app
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()  # infinte Loop

if __name__ == '__main__':
     main()
