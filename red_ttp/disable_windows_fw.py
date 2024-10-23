# Name: Disable Windows Firewall
# RTA: disable_windows_fw.py
# ATT&CK: T1089
# Description: Uses netsh.exe to backup, disable, and restore firewall rules.

import common
import os
import platform


def main():

    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("NetSH Advanced Firewall Configuration", log_type="~")
    netsh = "netsh.exe"
    rules_file = os.path.abspath("fw.rules")
    # Check to ensure that fw.rules does not already exist from a previous run
    common.remove_file(rules_file)
    # Back up the firewall rules
    common.log("Backing up rules")
    common.execute([netsh, "advfirewall", "export", rules_file])
    # Disable the firewall
    common.log("Disabling the firewall")
    common.execute([netsh, "advfirewall", "set", "allprofiles", "state", "off"])
    # Re-enable the firewall
    common.log("Enabling the firewall")
    common.execute([netsh, "advfirewall", "set", "allprofiles", "state", "on"])
    # Restore the original firewall rules
    common.log("Undoing the firewall change", log_type="-")
    common.execute([netsh, "advfirewall", "import", rules_file])
    # Remove the backup file
    common.remove_file(rules_file)


if __name__ == "__main__":
    exit(main())
