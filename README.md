**ACE Testing Framework**


**Steps for general use:**

WIP - only development functionality works, it is not ready for general use
1. Simply click on run_tests.bat and follow the instructions in the prompt that opens 


**Steps for getting everything set up for development:**
1. If you don't already have python installed, do that first. The latest version of python 3 from https://www.python.org is fine. Install it in the default location
2. Download PyCharm Community edition.
3. Open the ace-test-framework folder in PyCharm
4. Install the IntelliBot plugin (Settings > Plugins > Intellibot)
5. Install the following packages using pip (Go to Settings > Project: ace-test-framework > Project Interpreter > "+") (
Note: do **not** install in the user's site package directory):
- robotframework

6. Open cmd (the Command Prompt) and verify that you can run python and robot on the command line by typing

`$ python --version`

The version should be >= 3.0

`$ robot --version`

The version should be >= 3.0

If this works, you should also be able to go to
`$ cd path/to/ace-test/framework/robot/suites/bnc_card`
and execute `$ robot test_bnc_card.robot`

A window should open and then close after 10s (showing the format of the window that displays when running tests), and you should see new files under `robot/suites/bnc_card`
- `log.html`
- `output.html`
- `report.html`

Right click on `report.html`, then click "Open in Browser", select your browser of choice,
and voila! You have run a test suite and Robot Framework has automatically generated a test report for you!
You can click around in this report, see the different steps that were run, etc.

**Some useful info for development**
- Robot Framework (and its .robot files) are space sensitive. You need at least two spaces between keywords in order for them to work properly (any more than 2 spaces acts the same as 2 spaces). I (Joel) think we should have a convention of four or more spaces would be good to make it easy to see the different keywords


**Joel's placeholder for notes/to be implemented functionality**

You should be able to simply click on `run_tests.bat` within the root directory folder.
This will automatically run `python robot\shared\suiterunner\setup_and_run_suites.py` in cmd.
For now, this simply prints a message, waits two seconds, then exits, but I've left comments in setup_and_run_suites.py
that describe what we want to do within that function.
We might want to use the command window that is opened by default during the batch script to entering in relevant data (serial number, part name, etc.)
or simply outputting instructing for the techs about how to use/setup the system/hardware devices


Might be useful later (holding off for now):
- robotframework-debuglibrary

