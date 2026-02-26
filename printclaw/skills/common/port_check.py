import socket

from printclaw.core.context import AgentContext
from printclaw.core.registry import BaseSkill
from printclaw.core.results import SkillResult


class PortCheckSkill(BaseSkill):
    id = "network_port_check"
    name = "Port Check"
    description = "Check ports 9100/515/631"
    platform = "all"
    permission_level = "NETWORK_READ"

    def run(self, context: AgentContext) -> SkillResult:
        host = context.target_ip or "127.0.0.1"

        def open_port(port: int) -> bool:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.4)
                return sock.connect_ex((host, port)) == 0

        data = {
            "host": host,
            "port_9100_open": open_port(9100),
            "port_515_open": open_port(515),
            "port_631_open": open_port(631),
        }
        return SkillResult(skill_id=self.id, ok=True, message="Port check complete", data=data, evidence=[str(data)])
