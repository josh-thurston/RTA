"""
Name: Executable with Unusual Extensions
RTA: process_extension_anomalies.py
ATT&CK: T1036
Description:
The process_extension_anomalies.py script simulates creating processes with anomalous or uncommon file extensions
to mimic process masquerading techniques used in attacks. These extensions include `.com`, `.pif`, `.cmd`, and `.scr`.
Key Features:
- Anomalous Process Creation: Simulates process execution with unusual file extensions like `.com`, `.pif`, `.cmd`, and `.scr`.
- Process Masquerading: Copies an executable and renames it with these unusual extensions before execution.
- Windows-Specific: Since the script relies on Windows behavior for process execution and extensions, it should only run on Windows systems.
"""

import common
import platform

MY_APP = common.get_path("bin", "myapp.exe")


@common.dependencies(MY_APP)
def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    anomalies = [
        "evil.com",
        "bad.pif",
        "evil.cmd",
        "weird.scr"
    ]

    for path in anomalies:
        common.log("Masquerading python as %s" % path)
        common.copy_file(MY_APP, path)
        common.execute([path])
        common.remove_file(path)


if __name__ == "__main__":
    exit(main())
