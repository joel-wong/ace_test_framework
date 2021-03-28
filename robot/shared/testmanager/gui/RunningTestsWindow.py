from gui import BasicTestStatsWindow, BasicWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import signal
import os


class RunningTestsWindow(BasicTestStatsWindow.BasicTestStatsWindow):
    def __init__(self, window):
        super().__init__(window)
        self.stop_tests_after_suite_button = None
        self.stop_tests_immediately_button = None

        # Running tests text
        upper_spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(upper_spacer_item)
        self.running_tests_text = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(50)
        self.running_tests_text.setFont(font)
        self.running_tests_text.setStyleSheet("color: rgb(29, 116, 255);")
        self.verticalLayout.addWidget(self.running_tests_text, 0, QtCore.Qt.AlignHCenter)
        lower_spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(lower_spacer_item)

        # set up horizontal line for aesthetic purposes
        self.line_1 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        # add center grid layout (with test stats)
        self.verticalLayout.addLayout(self.gridLayout_1)

        # set up horizontal line for aesthetic purposes
        self.line_2 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        self.set_text()  # add relevant text

    def set_text(self):
        self.running_tests_text.setText("Running Tests...")

    def add_buttons(self, running_continuously):
        if running_continuously:
            # set up stop tests after current suite is finished button
            self.stop_tests_after_suite_button = BasicWindow.Button(self.centralwidget, self.verticalLayout, "red", "Normal Stop (After current suite finished)")
            self.stop_tests_after_suite_button.connect_button(self.stop_tests_after_suite)

        # set up stop tests immediately button
        self.stop_tests_immediately_button = BasicWindow.Button(self.centralwidget, self.verticalLayout, "red", "Emergency Stop")
        self.stop_tests_immediately_button.connect_button(lambda: self.stop_tests_immediately(running_continuously))

    def stop_tests_after_suite(self):
        self.running_tests_text.setText("Tests will stop after current suite is finished...")
        self.window.test_manager.stop_tests = True

    def stop_tests_immediately(self, running_continuously):
        self.running_tests_text.setText("Tests have stopped. Failing remaining tests...")
        if running_continuously:
            self.stop_tests_after_suite_button.button.setDisabled(True)
        if self.window.test_manager.robot_process.poll() is None:
            # send a ctrl+c signal to the running robot process to automatically
            # fail all remaining tests and stop running additional suites
            self.window.test_manager.stop_tests = True
            os.kill(self.window.test_manager.robot_process.pid, signal.CTRL_C_EVENT)
