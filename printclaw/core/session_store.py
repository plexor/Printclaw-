import json
from typing import Any

from sqlalchemy import select

from printclaw.db.database import SessionLocal, init_db
from printclaw.db.models import SessionRecord


class SessionStore:
    def __init__(self) -> None:
        init_db()

    def save(self, session_id: str, payload: dict[str, Any]) -> None:
        with SessionLocal() as db:
            rec = SessionRecord(session_id=session_id, payload_json=json.dumps(payload, default=str))
            db.merge(rec)
            db.commit()

    def list_sessions(self) -> list[dict[str, Any]]:
        with SessionLocal() as db:
            rows = db.execute(select(SessionRecord).order_by(SessionRecord.created_at.desc())).scalars()
            return [
                {
                    "session_id": row.session_id,
                    "created_at": row.created_at.isoformat(),
                }
                for row in rows
            ]

    def get(self, session_id: str) -> dict[str, Any] | None:
        with SessionLocal() as db:
            row = db.get(SessionRecord, session_id)
            if not row:
                return None
            return json.loads(row.payload_json)

    def delete(self, session_id: str) -> bool:
        with SessionLocal() as db:
            row = db.get(SessionRecord, session_id)
            if not row:
                return False
            db.delete(row)
            db.commit()
            return True
