"""
Name: Unexpected Network Activity from Microsoft Tools
RTA: unusual_ms_tool_network.py
ATT&CK: T1127
Description:
The unusual_ms_tool_network.py script generates network traffic from processes named after common Microsoft administration
and developer tools that typically do not initiate network connections unless being used maliciously.
Key Features:
- Simulated Network Activity: Creates HTTP GET requests using named processes such as `bginfo.exe`, `rcsi.exe`,
  `control.exe`, and `odbcconf.exe`.
- Deceptive Process Naming: Leverages the names of legitimate Microsoft tools to disguise malicious behavior.
- Windows-Specific: This script interacts with Windows executables and should only run on Windows systems.
"""

import os
import shutil
import sys
import platform
import common

process_names = [
    "bginfo.exe",
    "rcsi.exe",
    "control.exe",
    "odbcconf.exe"
]


def http_from_process(name, ip, port):
    path = os.path.join(common.BASE_DIR, name)
    common.log("Making HTTP GET from %s" % path)

    # Ensure the executable is copied correctly
    shutil.copy(str(sys.executable), str(path))  # Explicitly convert to string
    common.execute([str(path), "-c", f"import urllib; urllib.urlopen('http://{ip}:{port}')"])
    common.remove_file(path)


def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    server, ip, port = common.serve_web()

    for process in process_names:
        http_from_process(process, ip, port)

    server.shutdown()


if __name__ == "__main__":
    exit(main())
