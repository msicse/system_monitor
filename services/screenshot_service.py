from datetime import datetime
import mss, mss.tools
import logging

from config.settings import SCREENSHOT_DIR
from utils.paths_utils import get_screenshots_dir, ensure_dir
from utils.time_utils import timestamp

logger = logging.getLogger(__name__)


def take_screenshot():
    # Build target directory using utils
    target_dir = get_screenshots_dir(SCREENSHOT_DIR)
    ensure_dir(target_dir)

    saved_files = []

    try:
        with mss.mss() as sct:
            for idx, monitor in enumerate(sct.monitors[1:], start=1):

                # Generate filename
                filename = f"screenshot_{timestamp()}_{idx}.png"
                file_path = target_dir / filename

                # Capture
                screenshot = sct.grab(monitor)

                # Save file
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=str(file_path))
                saved_files.append(str(file_path))

        return saved_files

    except Exception as e:
        logger.exception("Screenshot failed: %s", e)
        return []
