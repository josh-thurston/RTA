# Red Team Automation (RTA)

RTA provides a framework of scripts designed to allow blue teams to test their detection capabilities against malicious tradecraft, modeled after [MITRE ATT&CK](https://attack.mitre.org/wiki/ATT&CK_Matrix).

RTA is composed of python scripts that generate evidence of over 50 different ATT&CK tactics, as well as a compiled binary application that performs activities such as file timestopping, process injections, and beacon simulation as needed.

Where possible, RTA attempts to perform the actual malicious activity described. In other cases, the RTAs will emulate all or parts of the activity. For example, some lateral movement will by default target local host (though with parameters typically allow for multi-host testing).  In other cases, executables such as cmd.exe or python.exe will be renamed to make it appeas as if a Windows binary is doing non-standard activities.

**Notice** This is a forked repository from teh original created by Endgame https://github.com/engameinc/RTA.  The original project appeared to be abandoned and has not had any updates in several years.  This forked repository was created so that the codee could be ported over to work with Python3

# Installation

## Prerequisites
 * Python3.8+


## Installation Steps
1) Download a copy of the RTA repo from https://github.com/josh-thurston/RTA.
2) Extract the contents of the zip archive into an RTA folder, such as c:\RTA  
3) For the full experience, download additional files into the bin subdirectory (as described in the dependencies section below)

## Dependencies
Some of the RTAs require 3rd party tools in order to execute properly. You can run many RTAs without additional tools, but to make use of the full suite, some will require additional downloads.

The following table provides dependency information:

| Dependency | RTAs | source |
| ---        | ---  | ---    |
| Sysinternals Suite | user_dir_escalation.py, sip_provider.py, system_restore_proc.py, trust_provider.py | [Microsoft](https://docs.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite) |
| MsXsl              | msxsl_network.py | [Microsoft](https://www.microsoft.com/en-us/download/details.aspx?id=21714) |


## Other Considerations
Windows Defender or other Anti-Virus products may block or otherwise interfere with RTAs while they run. Consider how you configure security products on the test host before running RTAs based on the goals of your tests.

## Customization
By modifying common.py, you can customize how RTA scripts will work in your environment. You could even write an entirely new function for use in one or more new RTAs.

# Running RTAs
To run the `powershell_args.py` RTA, simply run:
```commandline
python powershell_args.py
```

To run an entire directory of RTAs, the easiest way is to use the script-runner provided, "run_rta.py". This script-runner is capable of running every script in the "red_ttp" subdirectory and will do so by default:
"run_rta.py" has been updated to identify the platform/ OS and will only execute a script if it is on the correct platform. i.e. Windows script will not run on macOS or Linux etc.

**All operating systems:**
```commandline
python run_rta.py
```
