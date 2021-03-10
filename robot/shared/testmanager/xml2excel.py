from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Color
from xml_parser import *
import os

DEFAULT_FILENAME = "test_results.xlsx"
def default_file_path():
    return os.path.join(os.path.curdir, DEFAULT_FILENAME)
SHEET_TITLE = "TEST RESULTS SHEET: "
TEST_LIST_START_INDEX = 14
FAIL_COLOUR_HEX = 'ffab97'
PASS_COLOUR_HEX = '3c5e0b'

class Xml2Excel():
    def __init__(self,  robot_results_path, xlsx_file_path=default_file_path()):
        self.results_path = robot_results_path
        self.xlxs_file_path = xlsx_file_path
        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        self.suites = []

    def run(self):
        self.suites.append(parse_xml(self.results_path))
        # Title, Tester, Date, Approver
        self.insert_sheet_header()
        # Card/Suite Run Information
        self.insert_suite_info_headers()
        self.insert_suite_config_info()
        self.insert_test_results()

        # TODO: Add Parsed Data

        self.save_workbook()

    def insert_sheet_header(self):
        sheet_title = SHEET_TITLE + self.suites[0].suite_name
        self.insert_merged_title(sheet_title, 'A1', 'E1', bold=True, font_size=14)
        self.insert_element("Staff Member:", 'A2', bold=True)
        self.insert_element(str(self.suites[0].staff_name), 'B2')
        self.insert_element("Date:", 'A3', bold=True)
        self.insert_element(date_time_formatter(self.suites[0].date_time), 'B3')
        self.insert_element("Approver:", 'A4', bold=True)
        self.insert_element("Date:", 'A5', bold=True)

    def insert_suite_config_info(self):
        for suite in self.suites:
            self.insert_element(suite.part_number, 'A9')
            self.insert_element(suite.work_order_job_number, 'B9')
            self.insert_element(suite.batch_number, 'C9')
            self.insert_element(suite.serial_number, 'D9')
            #self.insert_element(suite.suite_name, 'E7')


    def insert_test_results(self):
        self.insert_merged_title("RESULTS", 'A12', 'E12', bold=True, font_size=12)
        self.insert_element("Status", 'A13', bold=True)
        self.insert_element("Test Runs", 'B13', bold=True)
        self.insert_element("Test Name", 'C13', bold=True)
        overall_status = True
        test_name_column = 'C'
        test_result_column = 'A'

        row = TEST_LIST_START_INDEX
        for test in self.suites[0].tests:
            name_cell = test_name_column + str(row)
            status_cell = test_result_column + str(row)
            self.insert_element(test.name, name_cell)
            self.insert_element(test.status, status_cell)
            if test.status == 'PASS':
                self.colour_cell(status_cell, PASS_COLOUR_HEX)
            else:
                self.colour_cell(status_cell, FAIL_COLOUR_HEX)
                overall_status = False
            row = row + 1

        row = row + 2
        self.insert_element("Overall Test Result:", 'A' + str(row), bold=True)
        overall_status_cell = 'B' + str(row)
        if overall_status:
            self.insert_element("PASS", overall_status_cell)
            self.colour_cell(overall_status_cell, PASS_COLOUR_HEX)
        else:
            self.insert_element("FAIL", overall_status_cell)
            self.colour_cell(overall_status_cell, FAIL_COLOUR_HEX)



    def insert_suite_info_headers(self):
        self.insert_merged_title("Card Information", 'A7', 'D7', font_size=12)
        self.insert_element("Part Number", 'A8', bold=True)
        self.insert_element("Work Order", 'B8', bold=True)
        self.insert_element("Batch Number", 'C8', bold=True)
        self.insert_element("Serial Number", 'D8', bold=True)


    def insert_element(self, text, element, bold=False):
        xlsx_element = self.worksheet[element]
        xlsx_element.font = Font(bold=bold)
        self.worksheet[element] = text

    def insert_merged_title(self, text, start_element, end_element, bold=True, font_size=11):
        start_element_cell = self.worksheet[start_element]
        start_element_cell.font = Font(bold=bold, size=font_size)
        self.worksheet[start_element] = text
        range = str(start_element) + ':' + str(end_element)
        self.worksheet.merge_cells(range)
        self.worksheet[start_element].alignment = Alignment(horizontal='center')

        #self.worksheet.merge_cells(range)

    def colour_cell(self, element, hex_colour):
        cell = self.worksheet[element]
        colour = Color(rgb=hex_colour)
        fill = PatternFill(patternType='solid', fgColor=colour)
        cell.fill = fill

    def save_workbook(self):
        self.workbook.save(self.xlxs_file_path)

def date_time_formatter(date_time_str):
    year = date_time_str[0:4]
    month = date_time_str[4:6]
    day = date_time_str[6:8]
    time = date_time_str[9:-1]
    formatted_str = year + "-" + month + "-" + day + ", " + time
    return formatted_str


def input_suit_info(suite_run_ifno):
    """
    Puts suite info into excel sheet
    :param SuiteRunInfo object
    """
    pass


if __name__ == "__main__":
    #test_list = parse_xml(data_source2)
    robot_results = "H:\\builds\Capstone\\ace-test-framework\out\\bnc_card\\2021-03-08T20-16-30-048130"
    xml_formatter = Xml2Excel(data_source3)
    xml_formatter.run()




