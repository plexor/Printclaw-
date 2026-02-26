from collections.abc import Iterable

from printclaw.core.context import AgentContext
from printclaw.core.results import SkillResult


class BaseSkill:
    id = "base"
    name = "Base Skill"
    description = ""
    platform = "all"
    permission_level = "READ_ONLY"
    requires_admin = False
    tags: list[str] = []

    def run(self, context: AgentContext) -> SkillResult:  # pragma: no cover
        raise NotImplementedError


class SkillRegistry:
    def __init__(self):
        self._skills: dict[str, BaseSkill] = {}

    def register(self, skill: BaseSkill) -> None:
        self._skills[skill.id] = skill

    def list(self) -> list[dict[str, str]]:
        return [
            {
                "id": skill.id,
                "name": skill.name,
                "description": skill.description,
                "platform": skill.platform,
                "permission_level": skill.permission_level,
            }
            for skill in self._skills.values()
        ]

    def run_all(self, context: AgentContext, skill_ids: Iterable[str] | None = None) -> list[SkillResult]:
        items = self._skills.items() if skill_ids is None else [(s, self._skills[s]) for s in skill_ids]
        return [skill.run(context) for _, skill in items]
