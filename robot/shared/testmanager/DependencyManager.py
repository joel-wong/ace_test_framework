import os
import subprocess
import sys


class DependencyManager:

    @staticmethod
    def install_dependencies():
        """Verifies dependencies needed for robot framework are installed"""

        # check python version and verify we are using Python 3
        if sys.version[0] < '3':
            print("ERROR: python version 3 required. You are using version "
                  "{}".format(sys.version))
            print("You must install python 3 from https://www.python.org")
            print("Make sure to check the 'pip' package manager option when")
            print("installing python")
            return
        try:
            import pip
        except ModuleNotFoundError:
            print("The python 'pip' package manager is required.")
            print("Go to https://www.python.org and download Python 3")
            print("When re-installing, select 'modify' and make sure")
            print("to check the 'pip' option")
            return

        print("Python 3 and pip is installed")

        # upgrade/install dependencies such as robot framework
        subprocess.run(["python", "-m", "pip", "install", "-q", "--user",
                        "--no-warn-script-location", "-r",
                        os.path.join(os.path.curdir, "requirements.txt")],
                       shell=True, check=True)
        print("Robot framework is installed and up to date")
        print("PyQT5 is installed and up to date")

    @staticmethod
    def upgrade_dependencies():
        """Upgrades dependencies to the latest version"""
        # upgrade pip
        print("Upgrading/installing any required dependencies...")
        subprocess.run(["python", "-m", "pip", "install", "--user",
                        "--upgrade", "pip", "--no-warn-script-location"],
                       shell=True, check=True)
        print("pip package manager has been upgraded to the latest version")

        # upgrade/install dependencies such as robot framework
        subprocess.run(["python", "-m", "pip", "install", "--user",
                        "--upgrade", "--no-warn-script-location", "-r",
                        os.path.join(os.path.curdir, "requirements.txt")],
                       shell=True, check=True)
        print("Robot framework has been upgraded to the latest version")
        print("PyQT5 has been upgraded to the latest version")


if __name__ == "__main__":
    dependency_manager = DependencyManager()
    dependency_manager.upgrade_dependencies()
