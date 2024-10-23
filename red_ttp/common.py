import subprocess
import socket
import time
import threading
import http.server
import binascii
import shutil
import sys
import socketserver
import re
import os
import getpass
import functools
import platform

try:
    HOSTNAME = socket.gethostname().lower()
    LOCAL_IP = socket.gethostbyname(HOSTNAME)
except socket.gaierror:
    LOCAL_IP = "127.0.0.1"

# Import Windows-specific modules only if running on Windows
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        winreg = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUCCESS = 0
GENERAL_ERROR = 1
MISSING_DEPENDENCIES = 2
MISSING_PSEXEC = 3
UNSUPPORTED_RTA = 4
ACCESS_DENIED = 5

USER_NAME = getpass.getuser().lower()

# PsExec utility for privilege escalation (only relevant for Windows)
PS_EXEC = os.path.join(BASE_DIR, "bin", "PsExec.exe") if platform.system() == "Windows" else None


# Function to get a path relative to the base directory
def get_path(*path):
    return os.path.join(BASE_DIR, *path)


# Simple logging function
def log(message, log_type='+'):
    print(f"[{log_type}] {message}")


# Check if the current user is SYSTEM (relevant for privilege escalation)
def check_system():
    return USER_NAME == "system" or USER_NAME.endswith("$")


# A function that only runs on Windows (example)
def run_system(arguments=None):
    if platform.system() != "Windows":
        log("This function requires Windows.")
        return UNSUPPORTED_RTA

    if check_system():
        return None

    if arguments is None:
        arguments = [sys.executable, os.path.abspath(sys.argv[0])] + sys.argv[1:]

    log("Attempting to elevate to SYSTEM using PsExec")
    if not os.path.exists(PS_EXEC):
        log("PsExec not found", log_type="-")
        return MISSING_PSEXEC

    p = subprocess.Popen([PS_EXEC, "-w", os.getcwd(), "-accepteula", "-s"] + arguments)
    p.wait()
    code = p.returncode
    if code == 5:
        log("Failed to escalate to SYSTEM", "!")
    return code


# Function to execute a command with options for logging and control over the process
def execute(command, hide_log=False, mute=False, timeout=30, wait=True, kill=False, drop=False, shell=False):
    """Execute a command and handle logging and output options."""
    if not hide_log:
        log(f"Executing: {command}")

    try:
        if shell:
            command = ' '.join(command) if isinstance(command, list) else command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        if wait:
            process.wait(timeout=timeout)
            stdout, stderr = process.communicate()
            return process.returncode, stdout.decode() + stderr.decode()
        return process.returncode, ''
    except subprocess.TimeoutExpired:
        log(f"Command timed out: {command}", log_type="!")
        return 1, ''
    except Exception as e:
        log(f"Failed to execute command: {e}", log_type="!")
        return 1, ''


def remove_file(file_path):
    """Removes a file if it exists."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            log(f"Removed file: {file_path}")
        except Exception as e:
            log(f"Failed to remove file {file_path}: {e}", log_type="!")
    else:
        log(f"File not found: {file_path}", log_type="-")


# Define 'dependencies' decorator
def dependencies(*required_files):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for file in required_files:
                if not os.path.exists(file):
                    log(f"Missing dependency: {file}", log_type="!")
                    return UNSUPPORTED_RTA
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Serve web content
def serve_web(port=8000):
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)

    log(f"Serving HTTP on port {port}")
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    ip = "127.0.0.1"  # Localhost
    return httpd, ip, port


# Clear web cache
def clear_web_cache():
    log("Clearing web cache (if applicable)")


# Function to replace a specific string (e.g., URL or port) in a file
def patch_file(original_file, old_string, new_string, target_file=None):
    if target_file is None:
        target_file = original_file

    try:
        with open(original_file, 'rb') as f:
            content = f.read()

        new_content = content.replace(old_string.encode(), new_string.encode())

        with open(target_file, 'wb') as f:
            f.write(new_content)

        log(f"Patched file: {original_file} -> {target_file}")

    except Exception as e:
        log(f"Failed to patch file {original_file}: {e}", log_type="!")


# Function to encode a string in wide characters (used for patching Windows binaries)
def wchar(text):
    return text.encode('utf-16le')


# Function to copy a file from source to destination
def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        log(f"Copied file from {source} to {destination}")
    except Exception as e:
        log(f"Failed to copy file {source} to {destination}: {e}", log_type="!")


# IP address regular expression
IP_REGEX = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'


# Find the remote host (this could be a hardcoded value or dynamically discovered)
def find_remote_host():
    # For testing, we might return a hardcoded remote host
    # You can modify this to dynamically discover or request input
    return "192.168.1.10"


# Get the IPv4 address of a hostname or host
def get_ipv4_address(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        log(f"Could not resolve IP address for {hostname}", log_type="!")
        return None


# Regex pattern to match callback URLs or similar patterns
CALLBACK_REGEX = r"http://[a-zA-Z0-9.-]+(:[0-9]+)?(/.*)?"


# Patch a file by finding a pattern using regex and replacing it with a new string
def patch_regex(file_path, pattern, replacement):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        new_content = re.sub(pattern, replacement, content)

        with open(file_path, 'w') as file:
            file.write(new_content)

        log(f"Patched file {file_path} with replacement pattern.")

    except Exception as e:
        log(f"Failed to patch file {file_path}: {e}", log_type="!")


def print_file(file_path):
    """Prints the content of a file to the console."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            log(f"Contents of {file_path}:\n{content}")
    except Exception as e:
        log(f"Failed to read file {file_path}: {e}", log_type="!")


# Path to the Windows command prompt (cmd.exe)
CMD_PATH = r"C:\Windows\System32\cmd.exe"


# Find a writable directory in the given path
def find_writeable_directory(base_path):
    """Finds a writable subdirectory within a base path."""
    for root, dirs, _ in os.walk(base_path):
        for directory in dirs:
            full_path = os.path.join(root, directory)
            if os.access(full_path, os.W_OK):
                log(f"Found writable directory: {full_path}")
                return full_path
    log(f"No writable directory found in {base_path}", log_type="-")
    return None


def is_64bit():
    """Check if the system is 64-bit."""
    return platform.machine().endswith('64')


def check_dependencies(target_program):
    """Check if the required target program exists."""
    return os.path.exists(target_program)
