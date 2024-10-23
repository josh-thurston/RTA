"""
Name: COM Hijack via Script Object
RTA: scrobj_com_hijack.py
ATT&CK: T1122
Description:
The scrobj_com_hijack.py script simulates creating a user-defined COM object that points to `scrobj.dll`. This technique is used by attackers to hijack COM objects for persistence or execution of malicious code.
Key Features:
- COM Object Hijacking: Modifies the Windows Registry to point a new CLSID to `scrobj.dll`, which can be used for persistence.
- Registry Modification: Adds and removes registry keys for COM object hijacking.
- Windows-Specific: This script modifies the Windows registry and should only run on Windows systems.
"""

import winreg as wreg
import platform
import common


def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    key = "SOFTWARE\\Classes\\CLSID\\{00000000-0000-0000-0000-0000DEADBEEF}\\InprocServer32"
    scrobj = "C:\\WINDOWS\\system32\\scrobj.dll"
    hkey = wreg.CreateKey(wreg.HKEY_CURRENT_USER, key)

    common.log("Setting up COM Server registry key")
    wreg.SetValue(hkey, "", wreg.REG_SZ, scrobj)

    common.log("Cleaning up COM Server from registry", log_type="-")
    wreg.DeleteValue(hkey, "")
    wreg.DeleteKey(hkey, "")
    wreg.CloseKey(hkey)

    hkey = wreg.CreateKey(wreg.HKEY_CURRENT_USER, "SOFTWARE\\Classes\\CLSID")
    wreg.DeleteKey(hkey, "{00000000-0000-0000-0000-0000DEADBEEF}")
    wreg.CloseKey(hkey)


if __name__ == "__main__":
    exit(main())
