"""
Name: Rundll32 Loading by Ordinal
RTA: rundll32_ordinal.py
ATT&CK: T1085
Description:
The rundll32_ordinal.py script simulates the use of `rundll32.exe` to load a DLL by ordinal. It executes the `dsquery.dll`
using ordinal loading, which is a technique that attackers may use to execute code through non-exported entry points.
Key Features:
- DLL Ordinal Loading: Executes the `dsquery.dll` using ordinal entry point loading with `rundll32.exe`.
- Simulates Suspicious Behavior: Copies a DLL file and runs it through an ordinal entry point.
- Windows-Specific: Since this script uses `rundll32.exe`, it should only run on Windows systems.
"""

import subprocess
import time
import shutil
import os
import platform
import common

RUNDLL32 = "rundll32.exe"


def run_dll(dll, entry_point):
    common.log("Running %s with %s and entrypoint %s" % (RUNDLL32, dll, entry_point))
    common.execute([RUNDLL32, dll, entry_point], timeout=3, kill=True)


@common.dependencies("C:\\Windows\\System32\\dsquery.dll")
def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("RunDLL32 with Ordinals")
    run_dll("dsquery.dll", "#258")
    dat_file = os.path.abspath("dsquery.dat")

    common.copy_file("C:\\Windows\\System32\\dsquery.dll", dat_file)
    run_dll(dat_file, "#258")
    time.sleep(2)
    common.remove_file(dat_file)


if __name__ == "__main__":
    exit(main())
