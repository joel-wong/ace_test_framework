from openpyxl import Workbook
from openpyxl.styles import Font
from xml_parser import *
import os

DEFAULT_FILENAME = "test_results.xlsx"
def default_file_path():
    return os.path.join(os.path.curdir, DEFAULT_FILENAME)
SHEET_TITLE = "TEST RESULTS SHEET"
PASS_COLOUR_HEX = 0xc5e0b3
FAIL_COLOUR_HEX = 0xffab97

class Xml2Excel():
    def __init__(self,  robot_results_path, xlsx_file_path=default_file_path()):
        self.results_path = robot_results_path
        self.xlxs_file_path = xlsx_file_path
        self.workbook = Workbook()
        self.worksheet = self.workbook.active

    def run(self):
        self.set_sheet_title()
        # TODO: Parse data

        self.save_workbook()

    def set_sheet_title(self, text=SHEET_TITLE, element='A1'):
        xlsx_element = self.worksheet[element]
        bold = Font(bold=True)
        xlsx_element.font = bold
        self.worksheet[element] = text

    def save_workbook(self):
        self.workbook.save(self.xlxs_file_path)


def input_suit_info(suite_run_ifno):
    """
    Puts suite info into excel sheet
    :param SuiteRunInfo object
    """
    pass


if __name__ == "__main__":
    test_list = parse_xml(data_source2)
    for test in test_list:
        print("Test Results: ")
        print("\tName: " + test.name)
        print("\tStatus: "+ test.status)
        pass
    robot_results = "H:\\builds\Capstone\\ace-test-framework\out\\bnc_card\\2021-03-08T20-16-30-048130"
    xml_formatter = Xml2Excel(robot_results)
    xml_formatter.run()




