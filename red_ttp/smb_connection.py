"""
Name: Outbound SMB from a User Process
RTA: smb_connection.py
ATT&CK: T1105
Description:
The smb_connection.py script initiates an SMB connection to a target machine without going through the normal Windows APIs.
This technique can be used for lateral movement and exploitation in Windows environments.
Key Features:
- Direct SMB Connection: Establishes a direct socket connection to a specified target on port 445.
- Customizable Target IP: Allows the user to specify the target IP for the SMB connection.
- Windows-Specific: This script utilizes SMB, which is specific to Windows environments.
"""

import socket
import sys
import platform
import common

SMB_PORT = 445


def main(ip=common.LOCAL_IP):
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    # connect to rpc
    common.log("Connecting to {}:{}".format(ip, SMB_PORT))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, SMB_PORT))
    common.log("Sending HELLO")
    s.send(b"HELLO!")  # Ensuring we send bytes
    common.log("Shutting down the connection...")
    s.close()
    common.log("Closed connection to {}:{}".format(ip, SMB_PORT))


if __name__ == "__main__":
    exit(main(*sys.argv[1:]))
