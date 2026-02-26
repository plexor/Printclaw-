from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SkillResult(BaseModel):
    skill_id: str
    ok: bool
    message: str
    data: dict[str, Any] = Field(default_factory=dict)
    evidence: list[str] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: datetime = Field(default_factory=datetime.utcnow)


class Issue(BaseModel):
    id: str
    category: str
    severity: str
    title: str
    description: str
    evidence: list[str] = Field(default_factory=list)


class FixRecommendation(BaseModel):
    id: str
    title: str
    description: str
    steps: list[str]
    requires_admin: bool
    estimated_success_probability: float
    command_preview: str | None = None
