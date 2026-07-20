from dataclasses import dataclass
from typing import List


@dataclass
class RootCause:

    id: str

    title: str

    severity: str

    confidence: float

    impact_score: int

    evidence: List[str]

    recommendation_ids: List[str]

