import platform


def detect_platform() -> str:
    return platform.system().lower()


def is_windows() -> bool:
    return detect_platform() == "windows"
