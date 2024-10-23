import os
import glob
import platform

RED_TTP_PATH = os.path.dirname(os.path.abspath(__file__))


def get_ttp_list(filter_by_os=True):
    """
    Returns a list of TTP scripts.
    :param filter_by_os: If True, filters scripts based on the current operating system.
    :return: List of script paths.
    """
    scripts = []
    current_os = platform.system() if filter_by_os else None

    for script in sorted(glob.glob(os.path.join(RED_TTP_PATH, "*.py"))):
        if os.path.basename(script) not in ("__init__.py", "common.py"):
            if filter_by_os:
                if "windows" in script.lower() and current_os != "Windows":
                    continue
                elif "linux" in script.lower() and current_os != "Linux":
                    continue
                elif "mac" in script.lower() and current_os != "Darwin":
                    continue
            scripts.append(script)
    return scripts


def get_ttp_names(filter_by_os=True):
    """
    Returns a list of TTP script names (without extensions).
    :param filter_by_os: If True, filters scripts based on the current operating system.
    :return: List of script names (without .py extension).
    """
    names = []
    for script in get_ttp_list(filter_by_os):
        basename, ext = os.path.splitext(os.path.basename(script))
        names.append(basename)
    return names
