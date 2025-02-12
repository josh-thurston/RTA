# Name: Downloading Files With Certutil
# RTA: certutil_webrequest.py
# ATT&CK: T1105
# Description: Uses certutil.exe to download a file.

import common
import platform

MY_DLL = common.get_path("bin", "mydll.dll")


@common.dependencies(MY_DLL)
def main():

    if platform.system() != 'Windows':
        common.log("This script only runs on Windows.")
        return common.UNSUPPORTED_RTA

    server, ip, port = common.serve_web()
    uri = "bin/mydll.dll"
    target_file = "mydll.dll"
    common.clear_web_cache()
    url = "http://{ip}:{port}/{uri}".format(ip=ip, port=port, uri=uri)
    common.execute(["certutil.exe", "-urlcache", "-split", "-f", url, target_file])
    server.shutdown()
    common.remove_file(target_file)


if __name__ == "__main__":
    exit(main())
