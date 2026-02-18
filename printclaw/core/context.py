from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from printclaw.core.constants import ExecutionMode


class AgentContext(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    execution_mode: ExecutionMode = ExecutionMode.SAFE_MODE
    confirm_actions: bool = True
    target_ip: str | None = None
