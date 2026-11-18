from dataclasses import dataclass

@dataclass
class MemoryRecord:
    id: int
    query: str
    answer: str
