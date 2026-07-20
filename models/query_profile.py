from dataclasses import dataclass, field
from typing import Dict, Any, List
from dataclasses import field
from models.query_info import QueryInfo
from models.timeline import Timeline
from models.exec_summary import ExecSummary


@dataclass
class QueryProfile:

    query_info: QueryInfo

    timeline: Timeline = field(
        default_factory=Timeline
    )

    statistics: Dict[str, Any] = field(
        default_factory=dict
    )

    authorization: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    scan_metrics: Dict[str, Any] = field(
        default_factory=dict
    )

    resource_metrics: Dict[str, Any] = field(
        default_factory=dict
    )

    memory_metrics: Dict[str, Any] = field(
        default_factory=dict
    )

    exec_summary: ExecSummary = field(
        default_factory=ExecSummary
    )

    resource_usage: Dict[str, Any] = field(
        default_factory=dict
    )

    fragment_instances: List[Any] = field(
        default_factory=list
    )

    cpu_metrics: list = field(
    default_factory=list
    )

    network_metrics: dict = field(
    default_factory=dict
    )

    operator_metrics: list = field(
    default_factory=list
    )


    raw_profile: str = ""

