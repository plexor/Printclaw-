from dataclasses import dataclass

from printclaw.core.constants import ExecutionMode


DENYLIST_KEYWORDS = [
    "format",
    "del /f",
    "rm -rf",
    "shutdown",
    "reg delete",
    "cipher /w",
    "diskpart",
    "bcdedit",
]


@dataclass
class SecurityPolicy:
    execution_mode: ExecutionMode = ExecutionMode.SAFE_MODE

    def check_command_text(self, command_preview: str) -> tuple[bool, str]:
        lowered = command_preview.lower()
        for keyword in DENYLIST_KEYWORDS:
            if keyword in lowered:
                return False, f"Blocked command due to denylisted keyword: {keyword}"
        if self.execution_mode == ExecutionMode.SAFE_MODE:
            return True, "SAFE_MODE requires explicit confirmation for mutating commands"
        return True, "Command allowed"
