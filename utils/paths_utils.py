from pathlib import Path
from datetime import datetime
import socket

def get_screenshot_dir(base_dir):
    hostname = socket.gethostname()
    today = datetime.now().strftime("%Y-%m-%d")
    return Path(base_dir) / hostname / today

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)