from __future__ import print_function

from PyQt5 import QtCore  # core Qt functionality
import sys  # we'll need this later to run our Qt application
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSlider, QApplication

from gl_widget import GLWidget
import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

import array
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import advertising

from gatt_server import GattServerMain

import argparse

import threading
import signal

class Simulator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        adapter_name = ''
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        self.__mainloop = GObject.MainLoop()

        advertising.advertising_main(self.__mainloop, bus, adapter_name)

        self.gatt_server = GattServerMain()
        self.gatt_server.gatt_server_main(self.__mainloop, bus, adapter_name)

    def run(self):
        print ("Starting Simulator")
        self.__mainloop.run()
        print ("Exiting Simulator")

    def update_rpy(self, roll: float, pitch: float, yaw: float):
        print(f"update_rpy {roll} {pitch} {yaw}")
        self.gatt_server.update_rpy(roll=roll, pitch=pitch, yaw=yaw)
    
    def destroy(self):
        self.__mainloop.quit()

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)  # call the init for the parent class

        self.resize(500, 500)
        self.setWindowTitle('Naqi Earbud Simulator')

        self.init_and_run_simulator()

        self.glWidget = GLWidget(self)
        self.init_gui()

        timer = QtCore.QTimer(self)
        timer.setInterval(20)  # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()

    def init_gui(self):
        central_widget = QWidget()
        gui_layout = QVBoxLayout()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

        slider_x = QSlider(QtCore.Qt.Horizontal)
        slider_x.valueChanged.connect(self.slider_x_valueChanged_handler)
        slider_x.setMinimum(-180)
        slider_x.setMaximum(180)

        slider_y = QSlider(QtCore.Qt.Horizontal)
        slider_y.valueChanged.connect(self.slider_y_valueChanged_handler)
        slider_y.setMinimum(-180)
        slider_y.setMaximum(180)

        slider_z = QSlider(QtCore.Qt.Horizontal)
        slider_z.valueChanged.connect(self.slider_z_valueChanged_handler)
        slider_z.setMinimum(-180)
        slider_z.setMaximum(180)

        gui_layout.addWidget(slider_x)
        gui_layout.addWidget(slider_y)
        gui_layout.addWidget(slider_z)
    
    def slider_x_valueChanged_handler(self, val):
        self.glWidget.setRotX(val)
        self.update_simulator()

    def slider_y_valueChanged_handler(self, val):
        self.glWidget.setRotY(val)
        self.update_simulator()

    def slider_z_valueChanged_handler(self, val):
        self.glWidget.setRotZ(val)
        self.update_simulator()

    def init_and_run_simulator(self):
        self.simulator = Simulator()
        self.simulator.start()
    
    def update_simulator(self):
        self.simulator.update_rpy(self.glWidget.getRotX(), self.glWidget.getRotY(), self.glWidget.getRotZ())

    def cleanup(self):
        self.simulator.destroy()

app = QApplication(sys.argv)
win = MainWindow()

def sigint_handler(*args):
    """
    Handler for the SIGINT signal.
    It is added here to intercept and handle CTRL-C
    """
    print("SIG_INT signal was caught")
    win.cleanup()
    app = QApplication.instance()
    app.quit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    win.show()
    sys.exit(app.exec_())