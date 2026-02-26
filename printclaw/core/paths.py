from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
KB_DIR = BASE_DIR / "knowledgebase"
DB_PATH = BASE_DIR / "db" / "printclaw.sqlite3"

for _path in [REPORTS_DIR, LOGS_DIR, DB_PATH.parent]:
    _path.mkdir(parents=True, exist_ok=True)
