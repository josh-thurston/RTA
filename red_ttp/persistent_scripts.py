# Name: Persistent Scripts
# RTA: persistent_scripts.py
# ATT&CK: T1064 (Scripting), T1086 (PowerShell)

import common
import os
import time
import platform

VBS = common.get_path("bin", "persistent_script.vbs")
NAME = "rta-vbs-persistence"


@common.dependencies(common.PS_EXEC, VBS)
def main():
    # Check if running on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("Persistent Scripts")

    if common.check_system():
        common.log("Must be run as a non-SYSTEM user", log_type="!")
        return 1

    # Remove any existing profiles
    user_profile = os.environ['USERPROFILE']
    log_file = os.path.join(user_profile, NAME + ".log")

    # Remove log file if exists
    common.remove_file(log_file)

    common.log("Running VBS")
    common.execute(["cscript.exe", VBS])

    # Let the script establish persistence, then read the log file back
    time.sleep(5)
    common.print_file(log_file)
    common.remove_file(log_file)

    # Now trigger a 'logon' event which causes persistence to run
    common.log("Simulating user logon and loading of profile")
    common.execute(["taskkill.exe", "/f", "/im", "explorer.exe"])
    time.sleep(2)

    common.execute(["C:\\Windows\\System32\\userinit.exe"], wait=True)
    common.execute(["schtasks.exe", "/run", "/tn", NAME])

    # Wait for the "logon" to finish
    time.sleep(30)
    common.print_file(log_file)

    # Cleanup
    common.log("Cleanup", log_type="-")
    common.remove_file(log_file)


if __name__ == "__main__":
    exit(main())
