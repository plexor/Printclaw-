from printclaw.core.results import Issue, SkillResult


class IssueEngine:
    def classify(self, skill_results: list[SkillResult]) -> list[Issue]:
        issues: list[Issue] = []
        by_id = {r.skill_id: r for r in skill_results}

        spooler = by_id.get("windows_spooler_status")
        if spooler and spooler.data.get("status", "").lower() != "running":
            issues.append(
                Issue(
                    id="issue_spooler_stopped",
                    category="SPOOLER",
                    severity="HIGH",
                    title="Spooler is stopped",
                    description="Printing is blocked because the spooler service is not running.",
                    evidence=spooler.evidence,
                )
            )

        jobs = by_id.get("windows_print_jobs")
        if jobs and jobs.data.get("total_jobs", 0) > 0:
            issues.append(
                Issue(
                    id="issue_queue_stuck",
                    category="QUEUE",
                    severity="MEDIUM",
                    title="Print queue has pending jobs",
                    description="Queue may be jammed with stuck print jobs.",
                    evidence=jobs.evidence,
                )
            )

        port = by_id.get("network_port_check")
        ping = by_id.get("network_ping")
        if ping and port and ping.data.get("reachable") and not port.data.get("port_9100_open"):
            issues.append(
                Issue(
                    id="issue_port_blocked",
                    category="NETWORK",
                    severity="HIGH",
                    title="Port 9100 closed while ping works",
                    description="Printer is reachable but print port is blocked or filtered.",
                    evidence=port.evidence,
                )
            )

        return issues
