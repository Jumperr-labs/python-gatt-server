from PyQt5 import QtCore  # core Qt functionality
import sys  # we'll need this later to run our Qt application
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSlider, QApplication

from gl_widget import GLWidget


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)  # call the init for the parent class

        self.resize(500, 500)
        self.setWindowTitle('Hello OpenGL App')

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
        slider_x.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        slider_y = QSlider(QtCore.Qt.Horizontal)
        slider_y.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        slider_z = QSlider(QtCore.Qt.Horizontal)
        slider_z.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))

        gui_layout.addWidget(slider_x)
        gui_layout.addWidget(slider_y)
        gui_layout.addWidget(slider_z)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())