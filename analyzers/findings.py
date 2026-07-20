# analyzers/findings.py

from dataclasses import dataclass
from typing import Dict, List, Union

@dataclass
class Finding:
    category: str
    severity: str
    title: str
    description: str
    evidence: Dict
    impact_score: int

def finding_to_dict(f):
    """Convert Finding dataclass to dict if needed."""
    if isinstance(f, Finding):
        return {
            "category": f.category,
            "severity": f.severity,
            "title": f.title,
            "description": f.description,
            "evidence": f.evidence,
            "impact_score": f.impact_score,
        }
    return f


def deduplicate_findings(findings: List[Union[Finding, dict]]) -> List[Union[Finding, dict]]:
    """
    Remove duplicate findings based on (category, title).
    Works for both Finding dataclass objects and plain dicts.
    """
    seen = set()
    unique = []
    for f in findings:
        # Handle both dataclass and dict
        if isinstance(f, Finding):
            key = (f.category, f.title)
        else:
            key = (f.get("category"), f.get("title"))

        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique

