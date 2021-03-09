from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.cell import cell
from xml_parser import *
import os

DEFAULT_FILENAME = "test_results.xlsx"
def default_file_path():
    return os.path.join(os.path.curdir, DEFAULT_FILENAME)
SHEET_TITLE = "TEST RESULTS SHEET"
BOLD = Font(bold=True)
PASS_COLOUR_HEX = 0xc5e0b3
FAIL_COLOUR_HEX = 0xffab97

class Xml2Excel():
    def __init__(self,  robot_results_path, xlsx_file_path=default_file_path()):
        self.results_path = robot_results_path
        self.xlxs_file_path = xlsx_file_path
        self.workbook = Workbook()
        self.worksheet = self.workbook.active

    def run(self):
        self.insert_title()
        self.insert_suite_info()
        # TODO: Parse data
        test_list, suite_info = parse_xml(self.results_path)
        for test in test_list:
            print("Test Results: ")
            print("\tName: " + test.name)
            print("\tStatus: " + test.status)

        self.save_workbook()

    def insert_suite_info(self):
        self.insert_merged_title("Card Information", 'A5', 'D5')
        self.insert_title("Part Number", 'A6')
        self.insert_title("Work Order", 'B6')
        self.insert_title("Batch Number", 'C6')
        self.insert_title("Serial Number", 'D6')



    def insert_title(self, text=SHEET_TITLE, element='A1'):
        xlsx_element = self.worksheet[element]
        xlsx_element.font = BOLD
        self.worksheet[element] = text

    def insert_merged_title(self, text, start_element, end_element, bold=True):
        if bold:
            start_element_cell = self.worksheet[start_element]
            start_element_cell.font = BOLD
        self.worksheet[start_element] = text
        range = str(start_element) + ':' + str(end_element)
        self.worksheet.merge_cells(range)
        self.worksheet[start_element].alignment = Alignment(horizontal='center')

        #self.worksheet.merge_cells(range)

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
    robot_results = "H:\\builds\Capstone\\ace-test-framework\out\\bnc_card\\2021-03-08T20-16-30-048130"
    xml_formatter = Xml2Excel(data_source2)
    xml_formatter.run()




