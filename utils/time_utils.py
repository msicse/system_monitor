from datetime import datetime


def timestamp() -> str:
    """
    Returns: 20251117_102305
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def time_only() -> str:
    """
    Returns: 102305 (HHMMSS)
    """
    return datetime.now().strftime("%H%M%S")


def readable_date() -> str:
    """
    Returns: 2025-11-17
    """
    return datetime.now().strftime("%Y-%m-%d")
