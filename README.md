# Printclaw

## What is Printclaw?
Printclaw is a local-first printer troubleshooting app with a real web GUI and CLI. It diagnoses printer issues, suggests fixes, and exports helpdesk-ready reports.

## Why it exists
Printer outages are noisy and expensive. Printclaw gives fast, safe, repeatable diagnostics for home, office, and MSP support teams.

## Features
- Dark dashboard GUI on localhost.
- Local sqlite session history.
- Export reports in JSON, TXT, and Markdown.
- Safe-mode defaults with confirmation-driven fixes.
- Skills system for printer, spooler, queue, and network checks.
- Knowledgebase search for vendor and error guidance.

## Screenshots (optional placeholder text, but do not break markdown)
Run the app and capture `/` after diagnostics.

## Install (Poetry)
```bash
poetry install
```

## Run Web GUI
```bash
poetry run printclaw web
```
Open `http://127.0.0.1:8080`.

## Run CLI Diagnostics
```bash
poetry run printclaw diagnose --export json
poetry run printclaw diagnose --export txt
poetry run printclaw diagnose --export md
```

## Safe Mode vs Apply Mode
- **SAFE_MODE** (default): no destructive action runs without explicit confirmation.
- **APPLY_MODE**: reserved for confirmed remediation workflows.

## How the Skill System Works
Skills implement `BaseSkill` and register in `SkillRegistry`. The agent runs skills, aggregates results, classifies issues, and proposes fixes.

## How Session History Works
Every diagnostic run is saved to sqlite with session payloads, including host context, issues, and recommendations.

## How Export Works
Reports are generated from saved sessions and exported as JSON/TXT/MD into `printclaw/reports/`.

## How to Add New Skills
1. Add a module under `printclaw/skills/...`.
2. Inherit `BaseSkill`.
3. Return `SkillResult` with evidence.
4. Register the skill in `PrintclawAgent`.

## Knowledgebase Format
Knowledgebase files are YAML with:
- `entries[]`
- `symptoms`
- `probable_cause`
- `recommended_fix_steps[]`

## Roadmap
- Electron wrapper for desktop packaging.
- Optional LLM reasoning with strict opt-in prompts.
- Expanded vendor-specific live checks.

## License
MIT.

## Example Commands
```bash
poetry install
poetry run printclaw web
poetry run printclaw diagnose --export json
poetry run printclaw sessions list
```

## Example ticket output
```text
Helpdesk Summary
Evidence:
- Spooler is stopped: Printing is blocked because the spooler service is not running.
Next Actions:
- Restart Print Spooler: Stop spooler
```
