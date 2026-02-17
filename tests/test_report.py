from printclaw.core.agent import PrintclawAgent
from printclaw.core.context import AgentContext


def test_report_builder_schema_keys():
    payload = PrintclawAgent().run_diagnostics(AgentContext())
    for key in ["timestamp", "session_id", "host", "printers", "skills_ran", "issues_found", "recommended_fixes", "confidence_score", "ticket_summary", "logs_path"]:
        assert key in payload
