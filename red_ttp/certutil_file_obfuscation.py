"""
Name: Certutil Encode / Decode
RTA: certutil_file_obfuscation.py
ATT&CK: T1140
Description:
The certutil_file_obfuscation.py script simulates the use of Certutil to encode and decode files.
It first encodes `cmd.exe` into an encoded file and then decodes it back, simulating how attackers
may obfuscate malicious files.
Key Features:
- File Encoding and Decoding: Uses `certutil.exe` to encode and decode files.
- Certutil Obfuscation: Simulates obfuscation of files to evade detection.
- Windows-Specific: Since `certutil.exe` is a Windows utility, this script should only run on Windows systems.
"""

import common
import os
import platform


def main():

    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("Encoding target")
    encoded_file = os.path.abspath('encoded.txt')
    decoded_file = os.path.abspath('decoded.exe')
    # Fixing path and formatting issues
    common.execute([r"c:\\Windows\\System32\\certutil.exe", "-encode", r"c:\\windows\\system32\\cmd.exe", encoded_file])
    common.log("Decoding target")
    common.execute([r"c:\\Windows\\System32\\certutil.exe", "-decode", encoded_file, decoded_file])
    common.log("Cleaning up")
    common.remove_file(encoded_file)
    common.remove_file(decoded_file)


if __name__ == "__main__":
    exit(main())
