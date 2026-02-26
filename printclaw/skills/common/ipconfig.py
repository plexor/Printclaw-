import platform
import subprocess

from printclaw.core.context import AgentContext
from printclaw.core.network_utils import local_ip_addresses
from printclaw.core.registry import BaseSkill
from printclaw.core.results import SkillResult


class IPConfigSkill(BaseSkill):
    id = "network_ipconfig"
    name = "IP Config"
    description = "Get local network info"
    platform = "all"
    permission_level = "READ_ONLY"

    def run(self, context: AgentContext) -> SkillResult:
        cmd = ["ipconfig"] if platform.system().lower() == "windows" else ["hostname", "-I"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return SkillResult(
            skill_id=self.id,
            ok=True,
            message="Collected local network details",
            data={"ips": local_ip_addresses()},
            evidence=[proc.stdout.strip()[:500]],
        )
