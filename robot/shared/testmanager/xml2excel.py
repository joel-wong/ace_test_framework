from openpyxl import Workbook
from openpyxl.styles import Font
from xml.dom import minidom

data_source = "H:\\builds\Capstone\\ace-test-framework\out\\bnc_card\\2021-03-08T20-16-30-048130\output.xml"

class TestStats:
    def __init__(self):
        test_status = None
        execution_time = None
        name = None
        test_number = None
        tag = None
        log = ""

class SuiteRunInfo:
    def __init__(self):
        suite_name = None
        part_number = None
        work_order = None
        batch_number = None
        serial_number = None
        tester = None
        date = None



def parse_xml(xml_file_path):
    test_list = []
    xml_file = minidom.parse(xml_file_path)
    items = xml_file.getElementsByTagName('test')
    for item in items:
        test = TestStats()
        test.name = item.attributes['name'].value

        #print(item.attributes['name'].value)
        test_status = item.getElementsByTagName('status')
        last_index = len(test_status) - 1

        test.status = test_status[last_index].attributes['status'].value

        test_list.append(test)

        #print("Overall Test Status: " + test_status[last_index].attributes['status'].value)
        #print(last_index)
        #for status in test_status:
        #  print(status.attributes['status'].value)
    return test_list

def input_suit_info(suite_run_ifno):
    """
    Puts suite info into excel sheet
    :param SuiteRunInfo object
    """





if __name__ == "__main__":
    test_list = parse_xml(data_source)
    for test in test_list:
        print("Test Results: ")
        print("\tName: " + test.name)
        print("\tStatus: "+ test.status)

    bold = Font(bold=True)

    wb = Workbook()
    ws = wb.active
    a1 = ws['A1']
    a1.font = bold
    ws['A1'] = "TEST RESULTS SHEET"
    wb.save("H:\\builds\Capstone\\ace-test-framework\out\\bnc_card\\2021-03-08T20-16-30-048130\\test.xlsx")
