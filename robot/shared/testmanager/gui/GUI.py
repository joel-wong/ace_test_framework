from gui import GUI_CONSTANTS
from gui.EnterSuiteWindow import EnterSuiteWindow
from gui.EnterMetadataWindow import EnterMetadataWindow
from gui.SelectTestsWindow import SelectTestsWindow
from gui.RunningTestsWindow import RunningTestsWindow
from gui.TestsCompleteWindow import TestsCompleteWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons


class TestRunnerWorker(QObject):
    def __init__(self, test_manager):
        super().__init__()
        self.test_manager = test_manager

    finished = pyqtSignal()
    progress = pyqtSignal()

    def run(self):
        self.test_manager.run_suites(self)
        self.finished.emit()


class GUI(QtWidgets.QStackedWidget):
    def __init__(self, test_manager):
        super().__init__()
        self.test_manager = test_manager

        self.enter_suite_window = EnterSuiteWindow(self)
        self.enter_metadata_window = EnterMetadataWindow(self)
        self.select_tests_window = SelectTestsWindow(self)
        self.running_tests_window = RunningTestsWindow(self)
        self.tests_complete_window = TestsCompleteWindow(self)
        self.thread = None
        self.worker = None

    def start_gui(self):
        self.addWidget(self.enter_suite_window)
        self.addWidget(self.enter_metadata_window)
        self.addWidget(self.select_tests_window)
        self.addWidget(self.running_tests_window)
        self.addWidget(self.tests_complete_window)
        self.resize(545, 385)
        self.setMaximumSize(QtCore.QSize(635, 475))
        self.setWindowTitle(GUI_CONSTANTS.APP_TITLE)
        self.show()

    def run_tests(self):
        self.thread = QThread()
        self.worker = TestRunnerWorker(self.test_manager)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.report_progress)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.finish)
        self.thread.start()

    def report_progress(self):
        self.running_tests_window.set_counts()

    def finish(self):
        self.tests_complete_window.set_counts()
        self.tests_complete_window.set_results_text()
        self.setCurrentIndex(self.currentIndex() + 1)
