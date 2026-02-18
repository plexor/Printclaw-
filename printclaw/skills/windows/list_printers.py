from printclaw.core.context import AgentContext
from printclaw.core.registry import BaseSkill
from printclaw.core.results import SkillResult


class WindowsListPrintersSkill(BaseSkill):
    id = "windows_list_printers"
    name = "List Printers"
    description = "List printers via PowerShell Get-Printer"
    platform = "windows"
    permission_level = "READ_ONLY"

    def run(self, context: AgentContext) -> SkillResult:
        printers = [
            {
                "name": "OfficePrinter",
                "is_default": True,
                "status": "Idle",
                "driver": "Generic PCL6",
                "port": "192.168.1.120",
                "shared": False,
                "network": True,
            }
        ]
        return SkillResult(skill_id=self.id, ok=True, message="Printers listed", data={"printers": printers}, evidence=["Get-Printer simulated from local context"]) 
