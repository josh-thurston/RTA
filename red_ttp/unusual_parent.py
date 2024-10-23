"""
Name: Invalid Process Trees in Windows
RTA: unusual_parent.py
ATT&CK: T1093
Description:
The unusual_parent.py script runs several Windows core processes directly, instead of from their proper parent in Windows.
This technique simulates suspicious behavior associated with process manipulation and bypassing standard operating procedures.
Key Features:
- Direct Process Execution: Executes core Windows processes like `winlogon.exe`, `lsass.exe`, etc., bypassing their usual parent processes.
- Simulates Malicious Activity: Demonstrates how attackers might manipulate process trees for nefarious purposes.
- Windows-Specific: This script relies on Windows executables and behavior, making it specific to Windows environments.
"""

import common
import os
import sys
import platform


def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("Running Windows processes with an unexpected parent of %s" % os.path.basename(sys.executable))
    process_names = [
        # "C:\\Windows\\System32\\smss.exe", BSOD (avoid this)
        # "C:\\Windows\\System32\\csrss.exe", BSOD (avoid this)
        # "C:\\Windows\\System32\\wininit.exe", BSOD (avoid this)
        # "C:\\Windows\\System32\\services.exe", BSOD (avoid this)
        "C:\\Windows\\System32\\winlogon.exe",
        "C:\\Windows\\System32\\lsass.exe",
        "C:\\Windows\\System32\\taskhost.exe",  # Win7
        "C:\\Windows\\System32\\svchost.exe",
    ]

    for process in process_names:
        # taskhostw.exe isn't on all versions of windows
        if os.path.exists(process):
            common.execute([process], timeout=2, kill=True)
        else:
            common.log("Skipping %s" % process, "-")


if __name__ == "__main__":
    exit(main())
