
from xml.dom import minidom

data_source = "H:\\builds\Capstone\\ace-test-framework\out\\bnc_card\\2021-03-08T20-16-30-048130\output.xml"
data_source2 = "H:\\builds\Capstone\\ace-test-framework\out\\bnc_card\\2021-03-09T01-47-34-182030\INDIVIDUAL TESTS\output-2021-03-09T01-47-34-183027.xml"
UNKNOWN_VALUE_ENTRY = "N/A"

class TestStats:
    def __init__(self):
        test_status = None
        execution_time = None
        name = None
        test_number = None
        tag = None
        log = ""

class SuiteRunInfo:
    def __init__(self, dict=None):
        if dict is not None:
            self.__dict__ = dict
            # Note: For this to work, it is expected for dict fields
            # to match attribute names in else clause
        else:
            suite_name = None
            serial_number = None
            batch_number = None
            part_number = None
            work_order_job_order = None
            staff_name = None
            include_manual_tests = None
            repeat_tests = None
            # date = None

def get_test_list(xml_minidom):
    test_list = []
    items = xml_minidom.getElementsByTagName('test')
    for item in items:
        test = TestStats()
        test.name = item.attributes['name'].value

        # print(item.attributes['name'].value)
        test_status = item.getElementsByTagName('status')
        last_index = len(test_status) - 1

        test.status = test_status[last_index].attributes['status'].value

        test_list.append(test)
    return test_list

def get_suite_info(xml_minidom):
    suites = xml_minidom.getElementsByTagName('suite')
    suite_info = []
    for suite in suites:
        doc = suite.getElementsByTagName('doc')
        if doc:
            last_index = len(doc) - 1  # suite doc stored in last element
            if doc[last_index].hasChildNodes():
                children = doc[last_index].childNodes
                for child in children:
                    suite_info.append(child.data)
                    suite_info = ''.join(suite_info)
    result = eval(suite_info)
    suite_info = SuiteRunInfo(result)
    return suite_info



def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def parse_xml(xml_file_path):
    suite_info = SuiteRunInfo()
    xml_file = minidom.parse(xml_file_path)
    test_list = get_test_list(xml_file)
    suite_info = get_suite_info(xml_file)
    return test_list