from dataclasses import (
    dataclass,
    field
)

@dataclass
class Config:
    Interval: int = 1
    Patterns: list[str] = field(default_factory=list)
