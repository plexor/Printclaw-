from printclaw.core.results import FixRecommendation, Issue


class FixEngine:
    def recommend(self, issues: list[Issue]) -> list[FixRecommendation]:
        fixes: list[FixRecommendation] = []
        for issue in issues:
            if issue.category == "SPOOLER":
                fixes.append(
                    FixRecommendation(
                        id="fix_restart_spooler",
                        title="Restart Print Spooler",
                        description="Restart the spooler service to restore printing.",
                        steps=["Stop spooler", "Start spooler", "Retry print"],
                        requires_admin=True,
                        estimated_success_probability=0.78,
                        command_preview="powershell Restart-Service Spooler",
                    )
                )
            elif issue.category == "QUEUE":
                fixes.append(
                    FixRecommendation(
                        id="fix_clear_queue",
                        title="Clear print queue",
                        description="Clear stuck queue jobs and resubmit print.",
                        steps=["Pause queue", "Remove jobs", "Resume queue"],
                        requires_admin=True,
                        estimated_success_probability=0.74,
                        command_preview="powershell Remove-PrintJob -PrinterName <name>",
                    )
                )
            elif issue.category == "NETWORK":
                fixes.append(
                    FixRecommendation(
                        id="fix_check_firewall",
                        title="Verify network printing ports",
                        description="Open 9100/515/631 on firewall and print server.",
                        steps=["Check firewall policy", "Allow printer ports", "Test again"],
                        requires_admin=True,
                        estimated_success_probability=0.62,
                        command_preview="netsh advfirewall show allprofiles",
                    )
                )
        return fixes
