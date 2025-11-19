from datetime import datetime
import os
import mss, mss.tools
import socket

from config.settings import SCREENSHOT_DIR






def take_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    today_date = datetime.now().strftime("%Y%m%d")
    screenshots = []
    hostname = socket.gethostname()
    target_dir = os.path.join(SCREENSHOT_DIR, hostname, today_date)
    
    os.makedirs(target_dir, exist_ok=True)

    try:
        with mss.mss() as sct:
            for idx, monitor in enumerate(sct.monitors[1:], start=1):
                screenshot = sct.grab(monitor)
                file_path = os.path.join(target_dir, f"screenshot_{timestamp}_{idx}.png")
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=file_path)
                screenshots.append(file_path)
        return screenshots
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return []
    

    safe_hostname = re.sub(r"[^A-Za-z0-9._-]", "_", hostname)



