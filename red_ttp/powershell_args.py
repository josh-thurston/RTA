"""
Name: Powershell with Suspicious Arguments
RTA: powershell_args.py
ATT&CK: T1140
Description:
The powershell_args.py script is designed to simulate calling PowerShell with suspicious command line arguments,
including executing commands using base64 encoding, bypassing execution policies, and running inline scripts.
Key Features:
- PowerShell Suspicious Commands: The script constructs and runs several PowerShell commands, including those with
suspicious arguments like -encodedCommand and -ExecutionPolicy Bypass.
- Temporary Script: It creates a temporary PowerShell script, executes it, and then cleans up the file.
- Windows-Specific: Since this script uses PowerShell, it should only run on Windows systems.
"""

import os
import base64
import platform
import common


def encode(command):
    return base64.b64encode(command.encode('utf-16le'))


def main():
    # Check if running on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("PowerShell Suspicious Commands")
    temp_script = os.path.abspath("tmp.ps1")

    # Create an empty script
    with open(temp_script, "w") as f:
        f.write("whoami.exe\n")

    powershell_commands = [
        'powershell -encoded %s' % encode('ping google.com').decode(),
        'powershell.exe -ExecutionPol Bypass %s' % temp_script,
        'powershell.exe iex Get-Process',
        'powershell.exe -ec %s' % encode('Get-Process' + ' ' * 1000).decode(),
    ]

    for command in powershell_commands:
        common.execute(command)

    common.remove_file(temp_script)


if __name__ == "__main__":
    exit(main())
