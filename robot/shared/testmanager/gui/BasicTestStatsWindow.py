from gui import BasicWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class TestStatDisplay:
    def __init__(self, central_widget, test_stat_text):
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text = QtWidgets.QLabel(central_widget)
        self.text.setFont(font)
        self.text.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text.setText(test_stat_text)

        self.count = QtWidgets.QLineEdit(central_widget)
        self.count.setMinimumSize(QtCore.QSize(0, 25))
        self.count.setAlignment(QtCore.Qt.AlignRight)
        self.count.setReadOnly(True)
        self.count.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.count.setFont(font)

    def set_count(self, x):
        self.count.setText(str(x))


class BasicTestStatsWindow(BasicWindow.BasicWindow):
    def __init__(self, window):
        super().__init__(window)

        # center grid layout within the vertical layout, add vertical spaces for aesthetic purposes
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.spacer_items = []
        for i in range(0, 4):
            self.spacer_items.append(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
            self.gridLayout_1.addItem(self.spacer_items[i], i * 2, 1)

        # Number of suite runs display
        self.suite_runs_stat_display = TestStatDisplay(self.centralwidget, "Number of suite runs:")
        self.add_test_stat_display(self.suite_runs_stat_display, row_num=1)

        # Number of tests failed display
        self.test_fail_stat_display = TestStatDisplay(self.centralwidget, "Number of tests failed:")
        self.add_test_stat_display(self.test_fail_stat_display, row_num=3)

        # Number of tests passed display
        self.test_pass_stat_display = TestStatDisplay(self.centralwidget, "Number of tests passed:")
        self.add_test_stat_display(self.test_pass_stat_display, row_num=5)

        self.set_counts()

    def set_counts(self):
        self.suite_runs_stat_display.set_count(self.window.test_manager.suite_count)
        self.test_fail_stat_display.set_count(self.window.test_manager.test_fail_count)
        self.test_pass_stat_display.set_count(self.window.test_manager.test_pass_count)

    def add_test_stat_display(self, test_stat_display, row_num):
        self.gridLayout_1.addWidget(test_stat_display.text, row_num, 0, QtCore.Qt.AlignLeft)
        self.gridLayout_1.addWidget(test_stat_display.count, row_num, 1)
