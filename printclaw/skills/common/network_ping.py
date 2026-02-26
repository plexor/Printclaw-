import platform
import subprocess

from printclaw.core.context import AgentContext
from printclaw.core.registry import BaseSkill
from printclaw.core.results import SkillResult


class NetworkPingSkill(BaseSkill):
    id = "network_ping"
    name = "Network Ping"
    description = "Ping printer IP"
    platform = "all"
    permission_level = "NETWORK_READ"
    tags = ["network", "ping"]

    def run(self, context: AgentContext) -> SkillResult:
        target = context.target_ip or "127.0.0.1"
        count_flag = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", count_flag, "1", target]
        process = subprocess.run(command, capture_output=True, text=True, check=False)
        reachable = process.returncode == 0
        return SkillResult(
            skill_id=self.id,
            ok=True,
            message="Ping executed",
            data={"target": target, "reachable": reachable},
            evidence=[process.stdout.strip()[:200] or process.stderr.strip()[:200]],
        )
