from enum import Enum


class ExecutionMode(str, Enum):
    SAFE_MODE = "SAFE_MODE"
    APPLY_MODE = "APPLY_MODE"


class PermissionLevel(str, Enum):
    READ_ONLY = "READ_ONLY"
    NETWORK_READ = "NETWORK_READ"
    SYSTEM_COMMANDS = "SYSTEM_COMMANDS"
    ADMIN_REQUIRED = "ADMIN_REQUIRED"
