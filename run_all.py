import time
import os
import red_ttp.common
import subprocess
import sys
import platform  # Add OS check logic

DELAY = 0


def main():
    errors = []
    current_os = platform.system()  # Get the current OS
    for ttp_file in red_ttp.get_ttp_list():
        print(("---- %s ----" % os.path.basename(ttp_file)))

        # Check if the script is Windows-only (for example)
        if "windows" in ttp_file.lower() and current_os != "Windows":
            print(f"Skipping {ttp_file} as it is Windows-specific.")
            continue
        elif "linux" in ttp_file.lower() and current_os != "Linux":
            print(f"Skipping {ttp_file} as it is Linux-specific.")
            continue
        elif "mac" in ttp_file.lower() and current_os != "Darwin":
            print(f"Skipping {ttp_file} as it is macOS-specific.")
            continue

        p = subprocess.Popen([sys.executable, ttp_file], shell=True)
        p.wait()
        code = p.returncode

        if p.returncode:
            errors.append((ttp_file, code))

        time.sleep(DELAY)
        print("")

    return len(errors)


if __name__ == "__main__":
    exit(main())
