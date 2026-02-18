# 🖨️ Printclaw

> **Local-first AI printer troubleshooting agent with a real GUI.**

Printclaw is a lightweight local app that diagnoses printer problems, suggests practical fixes, and generates helpdesk-ready reports you can share with IT.

---

## 📚 Table of Contents

- [What is Printclaw?](#-what-is-printclaw)
- [Why it exists](#-why-it-exists)
- [Features](#-features)
- [Quick Start](#-quick-start)
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

## 📦 Install (Poetry)

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

```bash
docker compose up --build
```

### 2) Open the app

Open: <http://127.0.0.1:8080>

### 3) Stop containers

```bash
docker compose down
```

### 4) Optional: run in background

```bash
docker compose up --build -d
```

### 5) Optional: follow logs

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
