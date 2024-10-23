"""
Name: Processes in Unusual Paths
RTA: unusual_process_path.py
ATT&CK: T1158
Description:
The unusual_process_path.py script executes processes from unusual directories, specifically targeting the WBEM
directory in Windows. This technique simulates running processes from unexpected locations to evade detection.
Key Features:
- Unusual Path Execution: Runs a specified program from a directory that is not typically used for executable files.
- Simulates Malicious Behavior: Demonstrates how attackers might execute malicious code from unexpected paths.
- Windows-Specific: This script interacts with Windows executables and should only run on Windows systems.
"""

import os
import platform
import common
import sys


def run_from_directory(target_program, directory):
    common.log("Running %s out of %s" % (target_program, directory))

    temp_path = os.path.join(directory, "temp-app.exe")
    common.copy_file(target_program, temp_path)
    common.execute([temp_path])
    common.remove_file(temp_path)


def main(target_program=common.get_path("bin", "myapp.exe")):
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("Processes in Unusual Paths")
    if not common.check_dependencies(target_program):
        return common.MISSING_DEPENDENCIES

    # user tmp
    directories = [
        "C:\\Windows\\system32\\wbem"
    ]

    for directory in directories:
        exists = os.path.exists(directory)
        if not exists:
            os.mkdir(directory)

        run_from_directory(target_program, directory)

        if not exists:
            os.rmdir(directory)


if __name__ == "__main__":
    exit(main(*sys.argv[1:]))
