from printclaw.core.context import AgentContext
from printclaw.core.registry import BaseSkill
from printclaw.core.results import SkillResult


class WindowsRestartSpoolerSkill(BaseSkill):
    id = "windows_restart_spooler"
    name = "Restart Spooler"
    description = "Restart spooler safely"
    platform = "windows"
    permission_level = "SYSTEM_COMMANDS"
    requires_admin = True

    def run(self, context: AgentContext) -> SkillResult:
        return SkillResult(skill_id=self.id, ok=True, message="Action requires confirmation before execution", data={"confirmed": False, "command": "Restart-Service Spooler"}, evidence=["Dry-run only"])
