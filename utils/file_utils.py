from pathlib import Path


def safe_delete(path):
    """
    Deletes a file safely (no error if missing).
    """
    try:
        Path(path).unlink()
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error deleting file {path}: {e}")


def file_exists(path) -> bool:
    return Path(path).exists()
