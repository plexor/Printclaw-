import json
from datetime import datetime
from pathlib import Path
from typing import Any

from printclaw.core.paths import REPORTS_DIR


class ReportBuilder:
    def build(self, session_payload: dict[str, Any]) -> dict[str, Any]:
        return session_payload

    def export(self, payload: dict[str, Any], fmt: str) -> Path:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        session_id = payload["session_id"]
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        path = REPORTS_DIR / f"report-{session_id}-{timestamp}.{fmt}"
        if fmt == "json":
            path.write_text(json.dumps(payload, indent=2, default=str))
        elif fmt == "txt":
            path.write_text(self._as_text(payload))
        elif fmt == "md":
            path.write_text(self._as_markdown(payload))
        else:
            raise ValueError(f"Unsupported export format: {fmt}")
        return path

    def _as_text(self, payload: dict[str, Any]) -> str:
        issues = "\n".join(f"- {i['title']} ({i['severity']})" for i in payload["issues_found"])
        fixes = "\n".join(f"- {f['title']} ({int(f['estimated_success_probability']*100)}%)" for f in payload["recommended_fixes"])
        return (
            f"Session: {payload['session_id']}\n"
            f"Timestamp: {payload['timestamp']}\n"
            f"Host: {payload['host']['hostname']} ({payload['host']['os']})\n\n"
            f"Issues Found:\n{issues or '- none'}\n\n"
            f"Recommended Fixes:\n{fixes or '- none'}\n\n"
            f"Ticket Summary:\n{payload['ticket_summary']}\n"
        )

    def _as_markdown(self, payload: dict[str, Any]) -> str:
        return (
            f"# Printclaw Report {payload['session_id']}\n\n"
            f"- **Timestamp:** {payload['timestamp']}\n"
            f"- **Host:** {payload['host']['hostname']} ({payload['host']['os']})\n"
            f"- **Confidence:** {payload['confidence_score']}\n\n"
            "## Issues\n"
            + "\n".join(f"- **{i['title']}** ({i['severity']}) - {i['description']}" for i in payload["issues_found"])
            + "\n\n## Recommended Fixes\n"
            + "\n".join(f"- **{f['title']}** - {f['description']}" for f in payload["recommended_fixes"])
            + f"\n\n## Ticket Summary\n{payload['ticket_summary']}\n"
        )
