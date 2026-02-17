from datetime import datetime

from printclaw.core.context import AgentContext
from printclaw.core.fix_engine import FixEngine
from printclaw.core.issue_engine import IssueEngine
from printclaw.core.kb_loader import KnowledgebaseLoader
from printclaw.core.network_utils import local_ip_addresses
from printclaw.core.registry import SkillRegistry
from printclaw.core.report_builder import ReportBuilder
from printclaw.core.session_store import SessionStore
from printclaw.core.utils import hostname, os_info
from printclaw.skills.common.ipconfig import IPConfigSkill
from printclaw.skills.common.network_ping import NetworkPingSkill
from printclaw.skills.common.port_check import PortCheckSkill
from printclaw.skills.windows.clear_queue import WindowsClearQueueSkill
from printclaw.skills.windows.event_logs import WindowsEventLogsSkill
from printclaw.skills.windows.list_printers import WindowsListPrintersSkill
from printclaw.skills.windows.print_jobs import WindowsPrintJobsSkill
from printclaw.skills.windows.restart_spooler import WindowsRestartSpoolerSkill
from printclaw.skills.windows.spooler_status import WindowsSpoolerStatusSkill


class PrintclawAgent:
    def __init__(self):
        self.registry = SkillRegistry()
        for skill in [
            WindowsListPrintersSkill(),
            WindowsSpoolerStatusSkill(),
            WindowsPrintJobsSkill(),
            WindowsRestartSpoolerSkill(),
            WindowsClearQueueSkill(),
            WindowsEventLogsSkill(),
            NetworkPingSkill(),
            PortCheckSkill(),
            IPConfigSkill(),
        ]:
            self.registry.register(skill)
        self.issue_engine = IssueEngine()
        self.fix_engine = FixEngine()
        self.report_builder = ReportBuilder()
        self.session_store = SessionStore()
        self.kb_loader = KnowledgebaseLoader()

    def run_diagnostics(self, context: AgentContext) -> dict:
        skill_results = self.registry.run_all(context)
        issues = self.issue_engine.classify(skill_results)
        fixes = self.fix_engine.recommend(issues)
        printers = next((r.data.get("printers", []) for r in skill_results if r.skill_id == "windows_list_printers"), [])
        confidence = max(35, 100 - 15 * len(issues))
        summary = self._ticket_summary(issues, fixes)
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": context.session_id,
            "host": {
                "os": os_info(),
                "hostname": hostname(),
                "user": "local-user",
                "ip_addresses": local_ip_addresses(),
            },
            "printers": printers,
            "skills_ran": [r.model_dump() for r in skill_results],
            "issues_found": [i.model_dump() for i in issues],
            "recommended_fixes": [f.model_dump() for f in fixes],
            "applied_fixes": [],
            "confidence_score": confidence,
            "ticket_summary": summary,
            "logs_path": "printclaw/logs/printclaw.log",
            "export_paths": {},
        }
        self.session_store.save(context.session_id, payload)
        return payload

    def _ticket_summary(self, issues, fixes) -> str:
        issue_lines = "\n".join([f"- {i.title}: {i.description}" for i in issues]) or "- No blocking issues found."
        fix_lines = "\n".join([f"- {f.title}: {f.steps[0]}" for f in fixes]) or "- No immediate fix required."
        return (
            "Helpdesk Summary\n"
            "Evidence:\n"
            f"{issue_lines}\n"
            "Next Actions:\n"
            f"{fix_lines}"
        )
