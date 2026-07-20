# extractors/registry.py

from extractors.memory_extractor import MemoryExtractor
from extractors.scan_extractor import ScanExtractor
from extractors.statistics_extractor import StatisticsExtractor
from extractors.operator_extractor import OperatorExtractor
from extractors.timeline_extractor import TimelineExtractor
from extractors.fragment_instance_extractor import FragmentInstanceExtractor
from extractors.network_extractor import NetworkExtractor
from extractors.metadata_extractor import MetadataExtractor
from extractors.exec_summary_extractor import ExecSummaryExtractor
from extractors.resource_extractor import ResourceExtractor
from extractors.summary_extractor import SummaryExtractor
from extractors.cpu_extractor import CPUExtractor

# Registry of all extractors
EXTRACTORS = [
    MemoryExtractor(),
    ScanExtractor(),
    StatisticsExtractor(),
    OperatorExtractor(),
    TimelineExtractor(),
    FragmentInstanceExtractor(),
    NetworkExtractor(),
    MetadataExtractor(),
    ExecSummaryExtractor(),
    ResourceExtractor(),
    SummaryExtractor(),
    CPUExtractor(),
]

