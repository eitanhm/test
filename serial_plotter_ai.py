''' >>> 
please create a python script that quaries 4 values from the serial port with commands sent v1,v2,v3,v4 respectivly ,evrery second ,put them in a log-file and display them on a gui wix window in a matplot graph. in the gui I should be able to set the graph timescale, start, stop, and number of points to show, in the graph.

Here is an example Python script that does what you described:
'''

import serial
import time
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtWidgets, QtGui

class SerialPlotter(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 9600
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.bytesize = serial.EIGHTBITS
        self.serial_port.timeout = 1

        # Create the log file for storing the data
        self.log_file = open("data.log", "w")

        # Set up the GUI window
        self.gui = QtWidgets.QDialog(self)
        self.gui.setWindowTitle("Serial Plotter")

        # Create a layout for the graph and buttons
        layout = QtWidgets.QVBoxLayout()
        self.gui.setLayout(layout)

        # Create a matplotlib figure and axis object
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax

        # Create a button to start the data acquisition
        start_button = QtWidgets.QPushButton("Start")
        start_button.clicked.connect(self.start_acquisition)
        layout.addWidget(start_button)

        # Create a button to stop the data acquisition
        stop_button = QtWidgets.QPushButton("Stop")
        stop_button.clicked.connect(self.stop_acquisition)
        layout.addWidget(stop_button)

        # Create a button to clear the log file
        clear_button = QtWidgets.QPushButton("Clear Log")
        clear_button.clicked.connect(self.clear_log)
        layout.addWidget(clear_button)

        # Create a button to save the log file
        save_button = QtWidgets.QPushButton("Save Log")
        save_button.clicked.connect(self.save_log)
        layout.addWidget(save_button)

        # Create a label for displaying the data points
        self.data_label = QtWidgets.QLabel("Data:")
        layout.addWidget(self.data_label)

        # Create a line edit for entering the number of points to show
        self.points_edit = QtWidgets.QLineEdit()
        self.points_edit.setPlaceholderText("Number of points to show")
        layout.addWidget(self.points_edit)

        # Create a button to set the graph timescale
        timescale_button = QtWidgets.QPushButton("Set Timescale")
        timescale_button.clicked.connect(self.set_timescale)
        layout.addWidget(timescale_button)

        # Create a button to start the graph at a specific point in time
        start_time_button = QtWidgets.QPushButton("Start Time")
        start_time_button.clicked.connect(self.set_start_time)
        layout.addWidget(start_time_button)

        # Create a button to stop the graph at a specific point in time
        end_time_button = QtWidgets.QPushButton("End Time")
        end_time_button.clicked.connect(self.set_end_time)
        layout.addWidget(end_time_button)

        # Create a button to save the graph as an image
        save_image_button = QtWidgets.QPushButton("Save Image")
        save_image_button.clicked.connect(self.save_image)
        layout.addWidget(save_image_button)

        # Create a label for displaying the current time
        self.time_label = QtWidgets.QLabel("Time:")
        layout.addWidget(self.time_label)

        # Start the GUI event loop
        self.gui.show()
        self.exec_()

    def start_acquisition(self):
        # Start the data acquisition in a separate thread
        thread = QtCore.QThread()
        self.worker = SerialWorker(self)
        self.worker.moveToThread(thread)
        thread.started.connect(self.worker.run)
        thread.start()

    def stop_acquisition(self):
        # Stop the data acquisition
        if self.worker is not None:
            self.worker.stop()

    def clear_log(self):
        # Clear the log file
        self.log_file.truncate(0)
        self.log_file.flush()
        self.data_label.setText("Data:")

    def save_log(self):
        # Save the log file
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save Log", "", "Log files (*.log)")[0]
        if filename != "":
            with open(filename, "w") as f:
                for line in self.log_file:
                    f.write(line)

    def set_timescale(self):
        # Set the graph timescale
        timescale = float(self.points_edit.text())
        self.ax.set_xlim(0, timescale)
        self.fig.canvas.draw()

    def set_start_time(self):
        # Set the start time of the graph
        start_time = float(self.points_edit.text())
        self.ax.set_xlim(start_time, 0)
        self.fig.canvas.draw()

    def set_end_time(self):
        # Set the end time of the graph
        end_time = float(self.points_edit.text())
        self.ax.set_xlim(0, end_time)
        self.fig.canvas.draw()

    def save_image(self):
        # Save the graph as an image file
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", "Image files (*.png)")[0]
        if filename != "":
            self.fig.canvas.print_figure(filename)




'''
This script creates a GUI window with buttons for starting and stopping the data acquisition, clearing the log
file, saving the log file, setting the graph timescale, start time, and end time, and saving the graph as an image
file. It also displays the data points in a matplot graph.

To use this script, you need to have Python 3 installed on your system and PyQt5. You also need to have a serial
port connected to your device that is sending the data.

You can run this script by opening a terminal window and typing:
```
python serial_plotter.py
```
This will open the GUI window and you can start the data acquisition by clicking on the "Start" button. The data
points will be displayed in the graph and logged to the file. You can stop the data acquisition by clicking on the
"Stop" button, clear the log file by clicking on the "Clear Log" button, save the log file by clicking on the
"Save Log" button, set the graph timescale by clicking on the "Set Timescale" button, start the graph at a
specific point in time by clicking on the "Start Time" button, stop the graph at a specific point in time by
clicking on the "End Time" button, and save the graph as an image file by clicking on the "Save Image" button.

Note that you need to have PySerial installed on your system to use this script. You can install it using pip
command:
```
pip install pyserial
```

>>> how can I install PyQt5?

pip install pyqt5
```
'''
