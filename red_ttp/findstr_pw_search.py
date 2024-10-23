# Name: Recursive Password Search
# RTA: findstr_pw_search.py
# ATT&CK: T1081
# Description: Recursively searches files looking for the string "password".

import common
import platform


def main():

    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    path = "c:\\"
    common.log("Searching for passwords on %s" % path)

    # Execute the findstr command to search for "password"
    common.execute("dir %s /s /b | findstr password" % path, shell=True)


if __name__ == "__main__":
    exit(main())
