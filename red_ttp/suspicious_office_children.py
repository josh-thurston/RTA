"""
Name: Emulate Suspect MS Office Child Processes
RTA: suspicious_office_children.py
ATT&CK: T1064
Description:
The suspicious_office_children.py script generates various child processes that can be spawned from emulated MS Office applications. This technique simulates suspicious behavior often associated with malicious activity.
Key Features:
- Emulates Child Processes: Simulates creating child processes from common MS Office applications like Word and Excel.
- Suspicious Command Execution: Runs potentially harmful commands through these emulated applications.
- Windows-Specific: This script relies on Windows executables and behavior, making it specific to Windows systems.
"""

import common
import os
import platform


def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("MS Office unusual child process emulation")
    suspicious_apps = [
        "msiexec.exe /i blah /quiet",
        "powershell.exe exit",
        "wscript.exe //b",
    ]
    cmd_path = "c:\\windows\\system32\\cmd.exe"

    for office_app in ["winword.exe", "excel.exe"]:
        common.log("Emulating %s" % office_app)
        office_path = os.path.abspath(office_app)
        common.copy_file(cmd_path, office_path)

        for command in suspicious_apps:
            common.execute('%s /c %s' % (office_path, command), timeout=5, kill=True)

        common.log('Cleanup %s' % office_path)
        common.remove_file(office_path)


if __name__ == "__main__":
    exit(main())
