"""
Name: RunDll32 with .inf Callback
RTA: rundll32_inf_callback.py
ATT&CK: T1105
Description:
The rundll32_inf_callback.py script simulates the use of RunDll32 with a suspicious .inf file, which triggers a local HTTP GET request. This can be used to simulate network callbacks from local system scripts.
Key Features:
- .inf File Callback: Executes RunDll32 with a .inf file that triggers a local network callback.
- Local HTTP Server: The script creates a web server to simulate receiving the callback request.
- Windows-Specific: This script uses `rundll32.exe`, making it specific to Windows systems.
"""

import time
import platform
import common

INF_FILE = common.get_path("bin", "script_launch.inf")


@common.dependencies(INF_FILE)
def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    # Start the HTTP server
    common.log("RunDLL32 with Script Object and Network Callback")
    server, ip, port = common.serve_web()
    callback = "http://%s:%d" % (ip, port)
    common.clear_web_cache()

    # Patch the .inf file with the callback URL
    common.patch_regex(INF_FILE, common.CALLBACK_REGEX, callback)

    rundll32 = "rundll32.exe"
    dll_entrypoint = "setupapi.dll,InstallHinfSection"
    common.execute([rundll32, dll_entrypoint, "DefaultInstall", "128", INF_FILE], shell=False)

    time.sleep(1)

    # Cleanup
    common.log("Cleanup", log_type="-")
    common.execute("taskkill /f /im notepad.exe")
    server.shutdown()


if __name__ == "__main__":
    exit(main())
