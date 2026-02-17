from printclaw.core.context import AgentContext
from printclaw.core.registry import BaseSkill
from printclaw.core.results import SkillResult


class WindowsClearQueueSkill(BaseSkill):
    id = "windows_clear_queue"
    name = "Clear Queue"
    description = "Clear print queue"
    platform = "windows"
    permission_level = "SYSTEM_COMMANDS"
    requires_admin = True

    def run(self, context: AgentContext) -> SkillResult:
        return SkillResult(skill_id=self.id, ok=True, message="Action requires confirmation before execution", data={"confirmed": False}, evidence=["Dry-run only"])
