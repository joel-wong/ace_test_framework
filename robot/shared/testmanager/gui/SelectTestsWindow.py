from gui import BasicWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from manual import MANUAL_TEST_CONSTANTS


class SelectTestsWindow(BasicWindow.BasicWindow):
    def __init__(self, window):
        super().__init__(window)
        self.config_manager = self.window.test_manager.config_manager
        self.test_list = None
        self.testTexts = None
        self.testBoxes = None
        self.selected_tests_list = ""

        # font size for central elements
        font = QtGui.QFont()
        font.setPointSize(10)

        # center scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setFont(font)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Select All Option
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.select_all_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font.setBold(True)
        font.setPointSize(12)
        self.select_all_text.setFont(font)
        self.select_all_text.setText("Select All")
        self.horizontalLayout.addWidget(self.select_all_text)
        self.select_all_box = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.select_all_box.setText("")
        self.horizontalLayout.addWidget(self.select_all_box, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_1.addLayout(self.horizontalLayout)

        # add scroll area
        self.verticalLayout.addWidget(self.scrollArea)

        # set up horizontal line for aesthetic purposes
        self.line_1 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        # set up start tests button
        self.start_tests_button = BasicWindow.Button(self.centralwidget, self.verticalLayout, "blue", "Start Tests")

        self.connect_buttons()  # connect buttons

    def display_test_list(self):
        self.test_list = self.window.test_manager.get_tests()
        num_tests = len(self.test_list)
        horizontalLayouts = []
        self.testTexts = []
        self.testBoxes = []
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        for i in range(num_tests):
            horizontalLayouts.append(QtWidgets.QHBoxLayout())
            self.testTexts.append(QtWidgets.QLabel(self.scrollAreaWidgetContents))
            if MANUAL_TEST_CONSTANTS.MANUAL_TEST_TAG in str(self.test_list[i].tags):
                self.testTexts[i].setText("{} {}".format(str(self.test_list[i]), MANUAL_TEST_CONSTANTS.MANUAL_TEST_NAME_INDICATOR))
            else:
                self.testTexts[i].setText(str(self.test_list[i]))
            self.testTexts[i].setWordWrap(True)
            self.testTexts[i].setSizePolicy(sizePolicy)
            horizontalLayouts[i].addWidget(self.testTexts[i])
            self.testBoxes.append(QtWidgets.QCheckBox(self.scrollAreaWidgetContents))
            self.testBoxes[i].setText("")
            horizontalLayouts[i].addWidget(self.testBoxes[i], 0, QtCore.Qt.AlignRight)
            self.verticalLayout_1.addLayout(horizontalLayouts[i])
        # connect select all checkbox
        # set default select all
        self.select_all_box.setChecked(True)
        for box in self.testBoxes:
            box.setChecked(True)
        self.select_all_box.stateChanged.connect(self.select_all)

    def select_all(self):
        for box in self.testBoxes:
            box.setChecked(self.select_all_box.isChecked())

    def connect_buttons(self):
        self.start_tests_button.connect_button(self.start_tests)

    def start_tests(self):
        include_manual = False
        for i in range(len(self.testBoxes)):
            if self.testBoxes[i].isChecked():
                self.selected_tests_list += "{}, ".format(self.test_list[i])
                if MANUAL_TEST_CONSTANTS.MANUAL_TEST_NAME_INDICATOR in self.testTexts[i].text():
                    include_manual = True
        if len(self.selected_tests_list) == 0:
            error_msg = BasicWindow.ErrorMessage("Please select at least one test!")
            return
        self.selected_tests_list = self.selected_tests_list[:len(self.selected_tests_list)-2]  # remove last comma and space
        if include_manual:
            include_manual_tests = "Y"
        else:
            include_manual_tests = "N"
        self.config_manager.set_config_value(self.config_manager.include_manual_tests_config, include_manual_tests)
        self.config_manager.save_config_as_default()
        self.window.setCurrentIndex(self.window.currentIndex() + 1)
        self.window.run_tests()
