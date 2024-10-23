"""
Name: Run Process from the Recycle Bin
RTA: recycle_bin_process.py
ATT&CK: T1158
Description:
The recycle_bin_process.py script simulates executing mock malware from the "C:\\Recycler\\" and "C:\\$RECYCLE.BIN\\"
subdirectories, which are often used by attackers to hide malicious processes.
Key Features:
- Recycle Bin Execution: Executes processes from the Recycle Bin directories, mimicking techniques used by malware to hide in the system.
- Simulates Process Execution: Runs an executable and command prompt (`cmd.exe`) from these hidden locations.
- Windows-Specific: The script relies on the Windows Recycle Bin directories, making it Windows-only.
"""

import common
import os
import time

RECYCLE_PATHS = ["C:\\$Recycle.Bin", "C:\\Recycler"]
TARGET_APP = common.get_path("bin", "myapp.exe")


@common.dependencies(TARGET_APP, common.CMD_PATH)
def main():
    common.log("Execute files from the Recycle Bin")
    target_dir = None
    for recycle_path in RECYCLE_PATHS:
        if os.path.exists(recycle_path):
            target_dir = common.find_writeable_directory(recycle_path)
            if target_dir:
                break

    else:
        common.log("Could not find a writeable directory in the recycle bin")
        exit(1)

    commands = [
        [TARGET_APP],
        [common.CMD_PATH, "/c", "echo hello world"],
    ]

    common.log("Running commands from recycle bin in %s" % target_dir)
    for command in commands:
        source_path = command[0]
        arguments = command[1:]

        target_path = os.path.join(target_dir, "recycled_process.exe")
        common.copy_file(source_path, target_path)
        arguments.insert(0, target_path)
        common.execute(arguments)
        time.sleep(2)
        common.remove_file(target_path)


if __name__ == "__main__":
    exit(main())
