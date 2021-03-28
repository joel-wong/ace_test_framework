from robot.api import SuiteVisitor, TestSuiteBuilder


class SelectTests(SuiteVisitor):
    def __init__(self, selected_test_list=None):
        self.tests = []
        if selected_test_list:
            self.selected_test_list = [test.strip() for test in selected_test_list.split(',')]
        else:
            self.selected_test_list = None

    def start_suite(self, suite):
        if self.selected_test_list:
            suite.tests = [t for t in suite.tests if self.is_included(t)]

    def is_included(self, test):
        return (str(test.name) in self.selected_test_list) or (str(test.longname) in self.selected_test_list)

    def visit_test(self, test):
        self.tests.append(test)


def get_tests(suite_directory):
    builder = TestSuiteBuilder()
    testsuite = builder.build(suite_directory)
    finder = SelectTests()
    testsuite.visit(finder)
    return finder.tests
