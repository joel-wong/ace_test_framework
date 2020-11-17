import time


def setup_and_run_suites():
    """Entry point to the ace-test-framework"""

    # For now, these comments just outline the different steps that we will use
    # TODO: Implement and test the commented steps

    # check python version and verify we are using Python 3

    # pip install pipenv if pipenv is not already installed

    # activate pipenv

    # pipenv install any required packages listed in the Pipfile
    # should simply be "pipenv install"

    # Check if there is an existing .aceoutputdir file (file name could change) or maybe an environmental variable
    # containing the output directory for the tests
    # We will use this to store the output directory for test results between test runs

    # if there is an existing .aceoutputdir file or env var, ask if the user would like to use that as the output path

    # if the user says yes, then check if that directory contains any past tests

    # if the user says no, ask them to enter a directory where the test results will be stored
    # copy this to .aceoutputdir file or env var

    # in either case, start asking the user for manual values
    # if there was a past test run, provide those values to the user as optional default values
    # the following values need to be received from the user:
    # - Serial number
    # - Part number
    # - Staff name
    # - Others?

    # List the test suites available to be run. Ask the user to type in the name of the test suite they want to run

    # store the values retrieved from the user in a .config file in the output directory specified by the user

    # run robot ../suites/{suite_name} --output {output directory} (perhaps with some other options)

    # these print and sleep statements are placeholders for now
    print("Executing setup_and_run_suites() in setup_and_run_suites.py")
    time.sleep(2)
    return 0


if __name__ == "__main__":
    setup_and_run_suites()
