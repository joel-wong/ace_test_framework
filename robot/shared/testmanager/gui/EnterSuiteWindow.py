from gui import BasicWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os


class EnterSuiteWindow(BasicWindow.BasicWindow):
    def __init__(self, window):
        super().__init__(window)
        self.config_manager = self.window.test_manager.config_manager

        # center grid layout within the vertical layout, add vertical spaces for aesthetic purposes
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.spacer_items = []
        for i in range(0, 2):
            self.spacer_items.append(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
            self.gridLayout_1.addItem(self.spacer_items[i], i * 2, 1)

        # font size for central elements
        font = QtGui.QFont()
        font.setPointSize(14)

        # suite name prompt and input box
        self.suite_name_text = QtWidgets.QLabel(self.centralwidget)
        self.suite_name_text.setFont(font)
        self.suite_name_text.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.gridLayout_1.addWidget(self.suite_name_text, 1, 0, QtCore.Qt.AlignRight)
        self.config_suite_name = QtWidgets.QComboBox(self.centralwidget)
        self.config_suite_name.setMinimumSize(QtCore.QSize(0, 25))
        self.config_suite_name.setFont(font)
        self.gridLayout_1.addWidget(self.config_suite_name, 1, 1)

        # add center grid layout
        self.verticalLayout.addLayout(self.gridLayout_1)

        # set up horizontal line for aesthetic purposes
        self.line_1 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        # set up choose folder section
        spacer_item3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item3)
        font.setPointSize(10)
        self.select_folder_text = QtWidgets.QLabel(self.centralwidget)
        self.select_folder_text.setFont(font)
        self.verticalLayout.addWidget(self.select_folder_text)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.folder_path = QtWidgets.QLineEdit(self.centralwidget)
        self.folder_path.setReadOnly(True)
        self.folder_path.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.folder_path.setFont(font)
        self.horizontalLayout_1.addWidget(self.folder_path)
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setFont(font)
        self.horizontalLayout_1.addWidget(self.browse_button)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        spacer_item4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item4)

        # set up horizontal line for aesthetic purposes
        self.line_2 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        # set up next button
        self.next_button = BasicWindow.Button(self.centralwidget, self.verticalLayout, "blue", "Next")

        self.set_text()  # add relevant text
        self.connect_buttons()  # connect buttons

    def set_text(self):
        self.suite_name_text.setText(self.config_manager.suite_name_config.gui_text)
        available_suites = self.config_manager.get_available_suites_and_set_suite_validator()
        for index in range(len(available_suites)):
            suite = available_suites[index].lower()
            self.config_suite_name.addItem(suite)
        default_suite = self.config_manager.get_default_config_value(self.config_manager.suite_name_config)
        if default_suite is not None:
            self.config_suite_name.setCurrentText(default_suite)

        self.select_folder_text.setText(self.config_manager.dir_path_config.gui_text)
        self.browse_button.setText("Browse")
        default_folder = self.config_manager.get_default_config_value(self.config_manager.dir_path_config)
        if default_folder is not None:
            self.folder_path.setText(default_folder)

    def connect_buttons(self):
        self.browse_button.clicked.connect(self.browse)
        self.next_button.connect_button(self.next)

    def browse(self):
        dir_path = os.path.abspath(QFileDialog.getExistingDirectory(self, "Choose Folder", "C:\\"))
        self.folder_path.setText(dir_path)

    def next(self):
        self.config_manager.set_config_value(self.config_manager.suite_name_config, self.config_suite_name.currentText())
        try:
            self.config_manager.set_config_value(self.config_manager.dir_path_config, self.folder_path.text())
        except AssertionError:
            error_msg = BasicWindow.ErrorMessage(self.config_manager.dir_path_config.gui_error_message)
            return
        self.window.setCurrentIndex(self.window.currentIndex() + 1)
