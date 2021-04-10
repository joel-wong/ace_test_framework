from gui import BasicTestStatsWindow, BasicWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import os


class TestsCompleteWindow(BasicTestStatsWindow.BasicTestStatsWindow):
    def __init__(self, window):
        super().__init__(window)

        # Set font for Test Complete text and Tests Results text
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(50)

        # Tests Complete text
        upper_spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(upper_spacer_item)
        self.tests_complete_text = QtWidgets.QLabel(self.centralwidget)
        self.tests_complete_text.setFont(font)
        self.verticalLayout.addWidget(self.tests_complete_text, 0, QtCore.Qt.AlignHCenter)

        # Tests Result text
        self.tests_result_text = QtWidgets.QLabel(self.centralwidget)
        self.tests_result_text.setFont(font)
        self.tests_result_text.setStyleSheet("color: rgb(0, 166, 80);")
        self.verticalLayout.addWidget(self.tests_result_text, 0, QtCore.Qt.AlignHCenter)
        lower_spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(lower_spacer_item)

        # set up horizontal line for aesthetic purposes
        self.line_1 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        # Display where test reports are saved
        self.test_reports_saved_in_text = QtWidgets.QLabel(self.centralwidget)
        font.setPointSize(12)
        self.test_reports_saved_in_text.setFont(font)
        self.verticalLayout.addWidget(self.test_reports_saved_in_text, 0, QtCore.Qt.AlignLeft)
        self.folder_path_button = QtWidgets.QPushButton(self.centralwidget)
        font.setPointSize(10)
        self.folder_path_button.setFont(font)
        self.verticalLayout.addWidget(self.folder_path_button)

        # Display link to open test report html
        self.test_report_excel_text = QtWidgets.QLabel(self.centralwidget)
        font.setPointSize(12)
        self.test_report_excel_text.setFont(font)
        self.verticalLayout.addWidget(self.test_report_excel_text, 0, QtCore.Qt.AlignLeft)
        self.excel_file_button = QtWidgets.QPushButton(self.centralwidget)
        font.setPointSize(10)
        self.excel_file_button.setFont(font)
        self.verticalLayout.addWidget(self.excel_file_button)

        # set up horizontal line for aesthetic purposes
        self.line_2 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        # add center grid layout (with test stats)
        self.verticalLayout.addLayout(self.gridLayout_1)

        # set up horizontal line for aesthetic purposes
        self.line_3 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        # Finish button
        self.finish_button = BasicWindow.Button(self.centralwidget, self.verticalLayout, "blue", "Finish")
        self.finish_button.connect_button(self.finish)

        self.set_text() # add relevant text

    def set_text(self):
        self.tests_complete_text.setText("Tests Complete!")
        self.test_reports_saved_in_text.setText("Test Reports Saved In:")
        self.test_report_excel_text.setText("Test Report Excel File:")

    def set_results_text(self):
        if self.window.test_manager.test_fail_count == 0:
            result = "All Tests Passed!"
            result_color = "color: rgb(0, 166, 80);"
        else:
            result = "Tests Failed"
            result_color = "color: rgb(255, 66, 19);"
        self.tests_result_text.setText(result)
        self.tests_result_text.setStyleSheet(result_color)

    def set_open_output_buttons(self, output_directory):
        self.output_directory = output_directory
        self.folder_path_button.setText(self.output_directory)
        self.folder_path_button.clicked.connect(self.open_folder)
        self.excel_file_button.setText(self.window.test_manager.get_excel_filename())
        self.excel_file_button.clicked.connect(self.open_excel)

    def open_folder(self):
        try:
            os.startfile(self.output_directory)
        except FileNotFoundError:
            error_msg = BasicWindow.ErrorMessage("Folder no longer exists!")
            return

    def open_excel(self):
        try:
            os.startfile(os.path.join(self.output_directory, self.window.test_manager.get_excel_filename()))
        except FileNotFoundError:
            error_msg = BasicWindow.ErrorMessage("File no longer exists!")
            return

    def finish(self):
        self.window.close()
