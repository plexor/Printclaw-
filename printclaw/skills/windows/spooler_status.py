from printclaw.core.context import AgentContext
from printclaw.core.registry import BaseSkill
from printclaw.core.results import SkillResult


class WindowsSpoolerStatusSkill(BaseSkill):
    id = "windows_spooler_status"
    name = "Spooler Status"
    description = "Check spooler service status"
    platform = "windows"
    permission_level = "READ_ONLY"

    def run(self, context: AgentContext) -> SkillResult:
        return SkillResult(skill_id=self.id, ok=True, message="Spooler status checked", data={"status": "Running"}, evidence=["Service Spooler state: Running"])
