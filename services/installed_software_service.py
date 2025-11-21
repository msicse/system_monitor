import winreg
import json

def list_installed_software():
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        r"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    software_list = []

    for path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        software = {}
                        for field in ["DisplayName", "DisplayVersion", "Publisher", "InstallDate", "InstallLocation", "UninstallString"]:
                            try:
                                value, _ = winreg.QueryValueEx(subkey, field)
                                software[field] = value
                            except FileNotFoundError:
                                software[field] = ""
                        if software.get("DisplayName"):
                            software_list.append(software)
        except FileNotFoundError:
            continue

    return software_list

def save_software_list_to_file(software_list, filename="data/installed_software.json"):
    if not software_list:
        print("No software found to save.")
        return
    
    with open(filename, "w") as f:
        json.dump(software_list, f, indent=4)


def check_blacklisted_software(software_list, cve_list):
    blacklisted_software = []
    for software in software_list:
        for cve in cve_list:
            if software.get("DisplayName") and cve.get("product") in software["DisplayName"]:
                blacklisted_software.append({
                    "software": software,
                    "cve": cve
                })
    return blacklisted_software


