# 🖨️ Printclaw

> **Local-first AI printer troubleshooting agent with a real GUI.**

Printclaw is a lightweight local app that diagnoses printer problems, suggests practical fixes, and generates helpdesk-ready reports you can share with IT.

---

## 📚 Table of Contents

- [What is Printclaw?](#-what-is-printclaw)
- [Why it exists](#-why-it-exists)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Install (Poetry)](#-install-poetry)
- [Run Web GUI](#-run-web-gui)
- [Docker Compose Setup and Run](#-docker-compose-setup-and-run)
- [Run CLI Diagnostics](#-run-cli-diagnostics)
- [CLI Command Reference](#-cli-command-reference)
- [Safe Mode vs Apply Mode](#-safe-mode-vs-apply-mode)
- [How the Skill System Works](#-how-the-skill-system-works)
- [How Session History Works](#-how-session-history-works)
- [How Export Works](#-how-export-works)
- [Knowledgebase Format](#-knowledgebase-format)
- [How to Add New Skills](#-how-to-add-new-skills)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Example Ticket Output](#-example-ticket-output)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## ❓ What is Printclaw?

Printclaw is a local-first printer diagnostics app with:

- A **web dashboard** for non-technical users.
- A **CLI** for technicians and IT operators.
- A **safe-by-default troubleshooting flow**.
- **Session history** stored locally in SQLite.
- **Exportable reports** in JSON, TXT, and Markdown.

It is designed to work even without a cloud LLM.

## 🎯 Why it exists

Printer outages are disruptive, expensive, and often repetitive. Printclaw exists to:

- Reduce time-to-diagnosis.
- Provide repeatable evidence for helpdesk escalation.
- Suggest fixes in a clear, practical order.
- Keep troubleshooting data local and private.

## ✨ Features

- Dark, responsive dashboard UI on localhost.
- Full diagnostic run with issues and recommended fixes.
- Session history saved automatically.
- Report export in JSON/TXT/MD.
- Skill-based architecture (Windows + network checks).
- Knowledgebase search for vendor and error patterns.
- Safe Mode execution defaults.

---

## 🚀 Quick Start

```bash
poetry install
poetry run printclaw web
```

Then open: <http://127.0.0.1:8080>

---

## 🧰 Prerequisites

Use the checklist for the run method you want:

### Windows (Poetry / local run)

- Windows 10 or Windows 11
- Python **3.11+** available in `PATH`
- [Poetry](https://python-poetry.org/docs/) installed
- PowerShell available (default on modern Windows)
- Optional for full Windows skill coverage: run terminal as Administrator when applying fixes

### macOS (Poetry / local run)

- macOS 12+ (Monterey or newer recommended)
- Python **3.11+** (via Homebrew, pyenv, or python.org installer)
- [Poetry](https://python-poetry.org/docs/) installed
- Build tools if needed by dependencies (`xcode-select --install`)

### Linux (Poetry / local run)

- Modern distro (Ubuntu 22.04+, Debian 12+, Fedora 39+, etc.)
- Python **3.11+**
- [Poetry](https://python-poetry.org/docs/) installed
- Typical build/runtime helpers: `pip`, `venv`, and `build-essential`/equivalent

### Docker (cross-platform)

- Docker Engine / Docker Desktop installed
- Docker Compose V2 (`docker compose` command)
- Port `8080` free on host

### Network/Printer access prerequisites (all methods)

- Host machine can reach target printer subnet
- Local firewall allows outbound diagnostics (`ping`, TCP checks)
- If diagnosing Windows spooler/service state, run on Windows for real native checks

---

## 📦 Install (Poetry)

## 📦 Install (Poetry)

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

## Screenshots 
Run the app and capture `/` after diagnostics.

## Install (Poetry)
```bash
poetry install
```

## 🌐 Run Web GUI

```bash
poetry run printclaw web
```

Open: <http://127.0.0.1:8080>

---

## 🐳 Docker Compose Setup and Run

Use Docker Compose if you want to run Printclaw in a containerized local environment.

### 1) Build and start

## Run Web GUI
```bash
poetry run printclaw web
```
Open `http://127.0.0.1:8080`.

## Docker Compose Setup and Run

Use Docker Compose if you want a containerized local run without managing a Poetry environment.

### 1) Build and start
```bash
docker compose up --build
```

### 2) Open the app

Open: <http://127.0.0.1:8080>

### 3) Stop containers

Go to `http://127.0.0.1:8080`.

### 3) Stop containers
```bash
docker compose down
```

### 4) Optional: run in background

```bash
docker compose up --build -d
```

### 5) Optional: follow logs

### 5) Optional: view logs
```bash
docker compose logs -f
```

---

## 🧪 Run CLI Diagnostics

```bash
poetry run printclaw diagnose --export json
poetry run printclaw diagnose --export txt
poetry run printclaw diagnose --export md
```

## 💻 CLI Command Reference

```bash
poetry run printclaw scan
poetry run printclaw diagnose
poetry run printclaw diagnose --export json
poetry run printclaw diagnose --export txt
poetry run printclaw diagnose --export md
poetry run printclaw sessions list
poetry run printclaw sessions show <id>
poetry run printclaw sessions export <id> --format json
poetry run printclaw kb search "spooler"
poetry run printclaw web
poetry run printclaw version
```

---

## 🔐 Safe Mode vs Apply Mode

- **SAFE_MODE** (default)
  - Prevents destructive actions unless explicitly confirmed.
  - Intended for diagnostics-first workflows.
- **APPLY_MODE**
  - Intended for confirmed remediation actions.
  - Use only when changes are approved.

## 🧠 How the Skill System Works

1. Skills inherit from `BaseSkill`.
2. Skills are registered in `SkillRegistry`.
3. The agent executes skills for a diagnostic session.
4. Results feed into issue classification and fix recommendation.
5. Evidence is saved in session history and included in reports.

## 🗂️ How Session History Works

Each diagnostic run is written to SQLite with key fields such as:

- `session_id`, `timestamp`
- host info (`os`, hostname, IPs)
- printers detected
- skill results and evidence
- issues found
- recommended/applied fixes
- confidence score
- ticket summary
- export paths

## 📄 How Export Works

Reports are generated from session data and saved under `printclaw/reports/`.

Supported formats:

- `json`
- `txt`
- `md`

## 📘 Knowledgebase Format

Knowledgebase files are YAML and use entries with:

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

Includes vendor files and common error/fix guidance.

## 🛠️ How to Add New Skills

1. Create a module under `printclaw/skills/...`.
2. Inherit `BaseSkill`.
3. Return a `SkillResult` with real evidence data.
4. Register the skill in the agent.
5. Add tests for behavior and expected output.

---

## 🧱 Project Structure

```text
printclaw/
  core/            # Agent orchestration, engines, safety, reports, sessions
  skills/          # Diagnostic and remediation skills
  web/             # FastAPI app, routes, templates, static assets
  knowledgebase/   # YAML troubleshooting knowledge
  db/              # SQLAlchemy database models and setup
  logs/            # Local logs
  reports/         # Exported session reports
tests/             # Automated tests
```

## 🖼️ Screenshots

Start the web UI and capture the dashboard after running diagnostics.

---

## 🧾 Example Ticket Output

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

## 🗺️ Roadmap

- Electron desktop wrapper for packaged distribution.
- Optional LLM reasoning with strict opt-in behavior.
- Expanded vendor/device-specific diagnostic skills.

## 📜 License

MIT
