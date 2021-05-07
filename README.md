# ACE Testing Framework #

This program simplifies and automates the testing of circuit cards.

The program first sets up a network connection to a BeagleBone.
Then, it will send the BeagleBone input and output specifications for a
series of tests.
During each test, the BeagleBone will apply the requested inputs and receive
the requested outputs from a circuit card that is attached to the BeagleBone.
The results will then be returned to this application and parsed in a
human-readable format.

## General Usage: ##

You will need Python version 3.7 or higher as well as pip installed in order to
run this program.

If you have Python 2 already installed, you must uninstall Python 2 before
installing Python 3. To do this, go to the Windows settings, then go to
"Add or Remove Programs", search for "Python 2", and uninstall the program.

If you don't have Python 3 or are unsure whether you have the correct version of
Python 3, you can download an installer for the latest version from
https://www.python.org/downloads/

The installer will automatically detect if you have Python 3 already installed.

If you do *not* have Python 3 installed, then click "install" and ensure that
the "add Python to PATH" and "pip" options are both selected. Note that "add
Python to PATH" is *excluded* by default and the "pip" option is *included* by
default. Also note that the options appear in different parts of the installer.

If you *do* have Python 3 already installed then click "modify" and install
"pip" if you do not have it already.

After Python and pip are installed, you need to double-click on 
`UpgradeDependencies.bat` to install any packages required to run the program.

Once that is done, you simply need to double-click on `RunTests.bat` and follow
the instructions in the graphical user interface (GUI) that opens to run the
tests!

To run the tests via the command-line with no GUI, the --nogui flag can be added
to the `RunTests.bat` file.

### Troubleshooting: ###
If the GUI doesn't appear, try running `UpgradeDependencies.bat` by
simply double-clicking on it before starting `RunTests.bat` again

If you are unable to connect to the BeagleBone, check the troubleshooting
steps in PTP-982-0105-002.




## Development Usage: ##
1. If you don't already have Python installed, install it first.
The latest version of Python 3 from https://www.python.org will work.
Install it in the default location
2. Download PyCharm Community edition.
3. Open the ace-test-framework folder in PyCharm
4. Install the IntelliBot plugin (Settings > Plugins > Intellibot)
5. Mark the following folders as "Sources Root" in PyCharm by right clicking on
   the folder in the Project window, then going to
   "Mark Directory As" > "Sources Root":
   - `robot/shared/lib`
   - `robot/shared/testmanager`
   - `Submodules`
6. Run `git submodule update --init --recursive` in the `ace-test-framework`
   folder
7. To run the tests with debug functionality in PyCharm, go to
`robot/shared/testmanager/TestManager.py` and then right click on the arrow to
the left of `if __name__ == "__main__":` at the very bottom of the file and
click "Debug ...". With this option, you will be able to put breakpoints in the
Python code which will allow you to inspect variable values, check code flows, etc.
8. You will likely want to exclude the "out" folder in Pycharm (this will be
automatically created after running tests). To do that, right click on the out
folder, then go to "Mark Directory As" > "Excluded"


### Using submodules ###

Git submodules allow code to be structured into separate blocks and reduce dependencies.
There is currently one submodule (ace-bbsm) in this project, and it is located
in the Submodules folder.

- Upon initially cloning the `ace-test-framework` repository, you must run
`git submodule update --init --recursive`
- To update your submodules, run `git submodule update`

### Modifying submodules: ###

In Git, go to Submodules\<your submodule name> (e.g. if using cmd
`cd Submodules/ace-bbsm`). Then, you can simply use all the standard git commands
(`git status`, `git commit`, etc.) and the submodule will act like a standard
Git repository.

After your changes to the submodule are complete, you can go to the main Git
repository (ace-test-framework) and simply call `git add Submodules/<submodule name>`
and `git commit` in order to have the main Git repository update its files to the
latest submodule version upon `git submodule update` being called


### Some useful info for development ###
- Robot Framework (and its .robot files) are space sensitive. You need at least
two spaces between keywords in order for them to work properly (any more than 2
spaces acts the same as 2 spaces). Our convention is to have four or more spaces
between keywords, which makes it easier to read
- If you need to debug robot framework, one method is adding
`Log To Console    ${variable name}` statements inside the robot code
