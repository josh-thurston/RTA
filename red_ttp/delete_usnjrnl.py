# Name: USN Journal Deletion with fsutil.exe
# RTA: delete_usnjrnl.py
# ATT&CK: T1107
# Description: Uses fsutil to delete the USN journal.

from . import common
import time
import platform


def main():

    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    message = "Deleting the USN journal may have unintended consequences"
    common.log("WARNING: %s" % message, log_type="!")
    # Execute the fsutil command to delete the USN journal
    common.execute(["fsutil", "usn", "deletejournal", "/d", "C:"])
    time.sleep(5)


if __name__ == "__main__":
    exit(main())
