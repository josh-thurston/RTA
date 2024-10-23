"""
Name: Process Execution in System Restore
RTA: system_restore_process.py
ATT&CK: T1158
Description:
The system_restore_process.py script copies mock malware into the System Volume Information directory and executes it.
This technique simulates evasion through the use of Windows' System Restore functionality.
Key Features:
- System Restore Evasion: Copies an executable to the System Volume Information directory to evade detection.
- Execution of Mock Malware: Executes the copied program, simulating a malicious process.
- Windows-Specific: This script interacts with Windows-specific features, making it suitable only for Windows systems.
"""

import os
import platform
import common

SYSTEM_RESTORE = "c:\\System Volume Information"


@common.dependencies(common.PS_EXEC)
def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    status = common.run_system()
    if status is not None:
        return status

    common.log("System Restore Process Evasion")
    program_path = common.get_path("bin", "myapp.exe")
    common.log("Finding a writable directory in %s" % SYSTEM_RESTORE)
    target_directory = common.find_writeable_directory(SYSTEM_RESTORE)

    if not target_directory:
        common.log("No writable directories in System Restore. Exiting...", "-")
        return common.UNSUPPORTED_RTA

    target_path = os.path.join(target_directory, "restore-process.exe")
    common.copy_file(program_path, target_path)
    common.execute(target_path)

    common.log("Cleanup", log_type="-")
    common.remove_file(target_path)


if __name__ == "__main__":
    exit(main())
