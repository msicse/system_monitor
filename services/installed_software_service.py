import winreg
import json
import logging
from pathlib import Path

from config.settings import DATA_DIR
from utils.paths_utils import get_reports_dir, ensure_dir

logger = logging.getLogger(__name__)

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

def save_software_list_to_file(software_list, filename=None):
    if not software_list:
        logger.warning("No software found to save.")
        return
    
    # Get the reports directory path
    reports_dir = get_reports_dir(DATA_DIR)
    ensure_dir(reports_dir)
    
    # Generate dated filename if not provided
    if filename is None:
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        dated_filename = f"software_{today}.json"
        latest_filename = "software.json"
        
        # Save dated version
        dated_path = reports_dir / dated_filename
        try:
            with open(dated_path, "w", encoding='utf-8') as f:
                json.dump(software_list, f, indent=4, ensure_ascii=False)
            logger.info(f"Dated software list saved to {dated_path}")
        except Exception as e:
            logger.error(f"Failed to save dated software list to {dated_path}: {e}")
            return None
        
        # Save/update latest version
        latest_path = reports_dir / latest_filename
        try:
            with open(latest_path, "w", encoding='utf-8') as f:
                json.dump(software_list, f, indent=4, ensure_ascii=False)
            logger.info(f"Latest software list saved to {latest_path} with {len(software_list)} entries")
            return str(latest_path)
        except Exception as e:
            logger.error(f"Failed to save latest software list to {latest_path}: {e}")
            return str(dated_path)  # Return dated path if latest fails
    
    # Custom filename provided
    file_path = reports_dir / filename
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(software_list, f, indent=4, ensure_ascii=False)
        logger.info(f"Software list saved to {file_path} with {len(software_list)} entries")
        return str(file_path)
    except Exception as e:
        logger.error(f"Failed to save software list to {file_path}: {e}")
        return None


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


