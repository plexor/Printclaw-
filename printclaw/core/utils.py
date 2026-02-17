import platform
import socket


def hostname() -> str:
    return socket.gethostname()


def os_info() -> str:
    return f"{platform.system()} {platform.release()}"
