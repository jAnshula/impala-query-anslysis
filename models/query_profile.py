from dataclasses import dataclass, field
from dataclasses import field
from models.query_info import QueryInfo
from models.timeline import Timeline
from models.exec_summary import ExecSummary
from typing import Dict, List, Optional, Any
from models.fragment_instance import FragmentInstance  # Import actual type
from models.cpu_metric import CPUMetric
from models.network_metric import NetworkMetric
from models.operator_metric import OperatorMetric


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

    fragment_instances: List[FragmentInstance] = field(
        default_factory=list
    )

    cpu_metrics: List[CPUMetric] = field(
        default_factory=list
    )

    network_metrics: Dict[str, Any] = field(
        default_factory=dict
    )
    
    operator_metrics: List[OperatorMetric] = field(
        default_factory=list
    )


    raw_profile: str = ""

