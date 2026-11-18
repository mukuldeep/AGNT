from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentContext:
    user_input: str
    history: list[dict[str, str]] = field(default_factory=list)
    observations: list[dict[str, Any]] = field(default_factory=list)
    step: int = 0
