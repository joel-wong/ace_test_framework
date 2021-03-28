from gui import GUI_CONSTANTS
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

BLUE_BUTTON_STYLESHEET = "background-color: rgb(172, 231, 255);"
RED_BUTTON_STYLESHEET = "background-color: rgb(255, 169, 158);"


class HorizontalLine:
    def __init__(self, central_widget, vertical_layout):
        self.line = QtWidgets.QFrame(central_widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        vertical_layout.addWidget(self.line)


class Button:
    def __init__(self, central_widget, vertical_layout, color, text):
        self.button = QtWidgets.QPushButton(central_widget)
        self.button.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.button.setFont(font)
        if color == "blue":
            self.button.setStyleSheet(BLUE_BUTTON_STYLESHEET)
        elif color == "red":
            self.button.setStyleSheet(RED_BUTTON_STYLESHEET)
        vertical_layout.addWidget(self.button)
        self.button.setText(text)

    def connect_button(self, function):
        self.button.clicked.connect(function)


class ErrorMessage:
    def __init__(self, error_text):
        self.error_msg = QMessageBox()
        self.error_msg.setIcon(QMessageBox.Warning)
        self.error_msg.setStandardButtons(QMessageBox.Retry)
        self.error_msg.setWindowTitle("Error")
        self.error_msg.setText(error_text)
        self.error_msg.exec_()


# Abstract class to be inherited by all GUI Window classes
class BasicWindow(QMainWindow):
    def __init__(self, window):
        super().__init__()
        self.window = window

        # set up layouts on the main window (main window base must be in grid
        # layout so everything dynamically resizes to the size of the main window)
        self.centralwidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        # set up app title
        self.app_title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(50)
        self.app_title.setFont(font)
        self.verticalLayout.addWidget(self.app_title, 0, QtCore.Qt.AlignHCenter)
        self.app_title.setText(GUI_CONSTANTS.APP_TITLE)

        # set up horizontal line for aesthetic purposes
        self.line_0 = HorizontalLine(self.centralwidget, self.verticalLayout)

        # Add layouts to main window
        self.gridLayout.addLayout(self.verticalLayout, 0, 0)
        self.setCentralWidget(self.centralwidget)
