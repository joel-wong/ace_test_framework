LISTENER_MESSAGE = 'Listener Message'
PASS_MESSAGE = 'PASS'
FAIL_MESSAGE = 'FAIL'


class Listener:
    ROBOT_LISTENER_API_VERSION = 3

    def end_test(self, data, result):
        if result.passed:
            print('\n{}:{}'.format(LISTENER_MESSAGE, PASS_MESSAGE))
        else:
            print('\n{}:{}'.format(LISTENER_MESSAGE, FAIL_MESSAGE))
