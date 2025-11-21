from pathlib import Path
from datetime import datetime
import socket

def get_hostname_base_dir(base_dir):
    """Get the base directory for a hostname: base_dir/hostname/"""
    hostname = socket.gethostname()
    return Path(base_dir) / hostname

def get_reports_dir(base_dir):
    """Get the reports directory: base_dir/hostname/reports/"""
    return get_hostname_base_dir(base_dir) / "reports"

def get_screenshots_dir(base_dir):
    """Get the screenshots directory: base_dir/hostname/screenshots/"""
    return get_hostname_base_dir(base_dir) / "screenshots"

# Legacy functions for backward compatibility (deprecated)
def get_screenshot_dir(base_dir):
    """Deprecated: Use get_screenshots_dir() instead"""
    return get_screenshots_dir(base_dir)

def get_data_dir(base_dir):
    """Deprecated: Use get_reports_dir() instead"""
    return get_reports_dir(base_dir)

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)