import shlex
import subprocess
from dataclasses import dataclass

from printclaw.core.constants import ExecutionMode
from printclaw.core.security import SecurityPolicy


@dataclass
class CommandOutcome:
    ok: bool
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    message: str


class SafeCommandRunner:
    def __init__(self, execution_mode: ExecutionMode = ExecutionMode.SAFE_MODE):
        self.policy = SecurityPolicy(execution_mode=execution_mode)
        self.allowlist = {"powershell", "ping", "tracert", "ipconfig", "net", "sc", "wmic"}

    def run(self, command: list[str], confirmed: bool = False) -> CommandOutcome:
        preview = " ".join(shlex.quote(part) for part in command)
        allowed, msg = self.policy.check_command_text(preview)
        if not allowed:
            return CommandOutcome(False, command, -1, "", msg, msg)
        if command[0].lower() not in self.allowlist:
            text = f"Command '{command[0]}' is not in allowlist"
            return CommandOutcome(False, command, -1, "", text, text)
        if self.policy.execution_mode == ExecutionMode.SAFE_MODE and not confirmed:
            text = "SAFE_MODE blocked execution until confirmation"
            return CommandOutcome(False, command, -1, "", text, text)
        process = subprocess.run(command, capture_output=True, text=True, shell=False, check=False)
        return CommandOutcome(
            ok=process.returncode == 0,
            command=command,
            returncode=process.returncode,
            stdout=process.stdout,
            stderr=process.stderr,
            message="completed" if process.returncode == 0 else "failed",
        )
