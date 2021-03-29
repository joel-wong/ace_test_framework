from xml.dom import minidom, Node
import json


UNKNOWN_VALUE_ENTRY = "N/A"

class TestStats:
    def __init__(self):
        self.test_status = UNKNOWN_VALUE_ENTRY
        self.execution_time = UNKNOWN_VALUE_ENTRY
        self.name = UNKNOWN_VALUE_ENTRY
        self.test_number = UNKNOWN_VALUE_ENTRY
        self.tag = UNKNOWN_VALUE_ENTRY


class SuiteRunInfo():
    def __init__(self, dict=None):
        if dict is not None:
            self.__dict__ = dict
            # Note: For this to work, it is expected for dict fields
            # to match attribute names in else clause
        else:
            self.suite_name = None
            self.serial_number = None
            self.batch_mo_number = None
            self.part_number = None
            self.work_order_job_number = None
            self.staff_name = None
            self.include_manual_tests = None
            self.repeat_tests = None
        self.tests = []


def get_test_list(xml_minidom):
    """
    Function that gets a list of TestStats objects using a xml_minidom object.
    Parses necessary data from xml minidom object

    :param xml_minidom: xml_minidom object
    :return: List of TestStats objects
    """
    test_list = []
    for element in xml_minidom.getElementsByTagName('test'):
        test = TestStats()
        # Get Test Name
        test.name = element.attributes['name'].value
        # Get Test Status (stored in last 'status' DOM)
        test_status = element.getElementsByTagName('status')
        last_index = len(test_status) - 1
        test.status = test_status[last_index].attributes['status'].value
        # Get Test Execution Time
        test.execution_time = test_status[last_index].attributes['endtime'].value

        for x in element.childNodes:
            if x.nodeType == Node.ELEMENT_NODE:
                if x.tagName == 'tag':
                    test.tag = x.childNodes[0].data
        test_list.append(test)

    return test_list


def get_suite_info(xml_minidom):
    """
    Function that creates SuiteRunInfo object using xml minidom object
    Parses necessary data from xml minidom object

    :param xml_minidom: xml_minidom object
    :return: SuiteRunInfo object
    """
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
    # Convert string to python dictionary
    result = json.loads(suite_info)
    suite_info = SuiteRunInfo(result)
    return suite_info


def parse_xml(xml_file_path):
    """
    Function that parses xml file and returns a SuiteRunInfo Object

    Creates a minidom object for the xml file and parses using function
    found in this file

    :param xml_file_path: String path to a .xml file
    :return: SuiteRunInfo object
    """
    xml_file = minidom.parse(xml_file_path)
    suite_info = get_suite_info(xml_file)
    test_list = get_test_list(xml_file)
    suite_info.tests = test_list
    suite_info.date_time = suite_info.tests[-1].execution_time
    return suite_info