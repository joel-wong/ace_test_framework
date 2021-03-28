from gui import BasicWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import ConfigManager


class MetadataDisplay:
    def __init__(self, central_widget, metadata_text):
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text = QtWidgets.QLabel(central_widget)
        self.text.setFont(font)
        self.text.setText(metadata_text)

        self.config = QtWidgets.QLineEdit(central_widget)
        self.config.setMinimumSize(QtCore.QSize(0, 25))
        self.config.setFont(font)

    def set_default_text(self, default):
        self.config.setText(default)

    def get_text(self):
        return self.config.text()


class EnterMetadataWindow(BasicWindow.BasicWindow):
    def __init__(self, window):
        super().__init__(window)
        self.config_manager = self.window.test_manager.config_manager
        self.errors = None

        # center grid layout within the vertical layout, add vertical spaces for aesthetic purposes
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.spacer_items = []
        for i in range(0, 7):
            self.spacer_items.append(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
            self.gridLayout_1.addItem(self.spacer_items[i], i*2, 1)

        self.metadata_display_types = [self.config_manager.part_number_config,
                                       self.config_manager.batch_mo_number_config,
                                       self.config_manager.serial_number_config,
                                       self.config_manager.work_order_job_number_config,
                                       self.config_manager.staff_name_config]
        self.metadata_displays = []
        for i, config_option in enumerate(self.metadata_display_types):
            self.metadata_displays.append(MetadataDisplay(self.centralwidget, config_option.gui_text))
            self.add_metadata_display(self.metadata_displays[i], row_num=i*2+1)

        font = QtGui.QFont()
        font.setPointSize(12)

        # Run tests continuously prompt and check box
        self.repeat_tests_text = QtWidgets.QLabel(self.centralwidget)
        self.repeat_tests_text.setFont(font)
        self.repeat_tests_text.setText(self.config_manager.repeat_tests_config.gui_text)
        self.gridLayout_1.addWidget(self.repeat_tests_text, 11, 0)
        self.repeat_tests_box = QtWidgets.QCheckBox(self.centralwidget)
        self.repeat_tests_box.setFont(font)
        self.gridLayout_1.addWidget(self.repeat_tests_box, 11, 1)

        # add center grid layout
        self.verticalLayout.addLayout(self.gridLayout_1)

        # set up horizontal line for aesthetic purposes
        self.line_1 = BasicWindow.HorizontalLine(self.centralwidget, self.verticalLayout)

        # set up next button
        self.next_button = BasicWindow.Button(self.centralwidget, self.verticalLayout, "blue", "Next")

        self.display_defaults()  # add relevant text
        self.connect_buttons()  # connect buttons

    def add_metadata_display(self, metadata_display, row_num):
        self.gridLayout_1.addWidget(metadata_display.text, row_num, 0, QtCore.Qt.AlignLeft)
        self.gridLayout_1.addWidget(metadata_display.config, row_num, 1)

    def display_defaults(self):
        for i, config_option in enumerate(self.metadata_display_types):
            self.set_default_text(config_option, self.metadata_displays[i])
        if self.config_manager.get_bool(ConfigManager.CONFIG_REPEAT_TESTS):
            self.repeat_tests_box.setChecked(True)

    def set_default_text(self, config_type, metadata_display):
        default = self.config_manager.get_default_config_value(config_type)
        if default is not None:
            metadata_display.set_default_text(str(default))

    def connect_buttons(self):
        self.next_button.connect_button(self.next)

    def next(self):
        self.errors = []
        self.check_and_set_inputs()
        if len(self.errors) > 0:
            error_text = ""
            for e in self.errors:
                error_text += e + '\n'
            error_msg = BasicWindow.ErrorMessage(error_text)
            return
        self.window.select_tests_window.display_test_list()
        self.window.setCurrentIndex(self.window.currentIndex() + 1)
        self.window.running_tests_window.add_buttons(self.config_manager.get_bool(ConfigManager.CONFIG_REPEAT_TESTS))

    def check_and_set_inputs(self):
        for i, config_option in enumerate(self.metadata_display_types):
            try:
                self.config_manager.set_config_value(config_option, self.metadata_displays[i].get_text())
            except AssertionError:
                self.errors.append(config_option.gui_error_message)
        if self.repeat_tests_box.isChecked():
            repeat_tests = "Y"
        else:
            repeat_tests = "N"
        self.config_manager.set_config_value(self.config_manager.repeat_tests_config, repeat_tests)
