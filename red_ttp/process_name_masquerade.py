"""
Name: Windows Core Process Masquerade
RTA: process_name_masquerade.py
ATT&CK: T1036
Description:
The process_name_masquerade.py script simulates process masquerading by creating processes with names commonly used
by legitimate core Windows processes (e.g., `svchost.exe`, `lsass.exe`, etc.) but executing a different program.
Key Features:
- Process Masquerading: Creates processes with names like `svchost.exe`, `lsass.exe`, and `services.exe` to simulate masquerading.
- Simulates Suspicious Process Behavior: Executes a custom executable under the guise of a legitimate Windows process name.
- Windows-Specific: Since these names are associated with Windows core processes, this script should only run on Windows systems.
"""

import os
import platform
import common

MY_APP = common.get_path("bin", "myapp.exe")


@common.dependencies(MY_APP)
def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    masquerades = [
        "svchost.exe",
        "lsass.exe",
        "services.exe",
        "csrss.exe",
    ]

    for name in masquerades:
        path = os.path.abspath(name)
        common.copy_file(MY_APP, path)
        common.execute(path, timeout=3, kill=True)
        common.remove_file(path)


if __name__ == "__main__":
    exit(main())
