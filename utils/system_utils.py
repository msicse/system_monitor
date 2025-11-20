import socket
import platform


def get_hostname() -> str:
    return socket.gethostname()


def get_os_info() -> str:
    return platform.platform()


def get_username() -> str:
    try:
        import getpass
        return getpass.getuser()
    except:
        return "unknown"
def is_windows() -> bool:
    return platform.system().lower() == "windows"