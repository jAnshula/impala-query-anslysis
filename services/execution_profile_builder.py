from models.query_profile import QueryProfile

from extractors.summary_extractor import (
    SummaryExtractor
)

from extractors.timeline_extractor import (
    TimelineExtractor
)

from extractors.metadata_extractor import (
    MetadataExtractor
)

from extractors.exec_summary_extractor import (
    ExecSummaryExtractor
)


from extractors.fragment_instance_extractor import (
    FragmentInstanceExtractor
)

from extractors.scan_extractor import (
    ScanExtractor
)

from extractors.resource_extractor import (
    ResourceExtractor
)

from extractors.memory_extractor import (
    MemoryExtractor
)

from extractors.operator_extractor import (
    OperatorExtractor
)

from extractors.cpu_extractor import (
    CPUExtractor
)

from extractors.network_extractor import (
    NetworkExtractor
)

from analyzers.execution_analyzer import (
    ExecutionAnalyzer
)

def sanitize_timeline(timeline):
    planning = max(timeline.get("planning_ms", 0) or 0, 0)
    admission = max(timeline.get("admission_ms", 0) or 0, 0)
    execution = max(timeline.get("execution_ms", 0) or 0, 0)

    # If execution is missing or negative, recompute safely
    total = timeline.get("total_ms", planning + admission + execution)
    if execution <= 0 and total > 0:
        derived = total - planning - admission
        execution = max(derived, 0)

    return {
        "planning_ms": planning,
        "admission_ms": admission,
        "execution_ms": execution,
        "total_ms": planning + admission + execution,
        "events": {
            "planning_ms": planning,
            "admission_ms": admission,
            "execution_ms": execution,
        }
    }

class ExecutionProfileBuilder:
    def build(self, text):
        query_info = SummaryExtractor().parse(text)
        timeline = TimelineExtractor().parse(text)
        metadata = MetadataExtractor().parse(text)

        scan_metrics = ScanExtractor().parse(text)
        resource_metrics = ResourceExtractor().parse(text)

        fragment_instances = FragmentInstanceExtractor().parse(
            text,
            query_info.query_id
        )

        memory_metrics = MemoryExtractor().parse(text)

        # Fallback if memory extractor found nothing
        if memory_metrics.get("peak_memory_mb", 0) == 0:

            execution_analyzer = ExecutionAnalyzer()

            fragment_summary = (
                execution_analyzer.fragment_summary(
                    fragment_instances
                )
            )

            peak_summary = (
                execution_analyzer.peak_memory_summary(
                    fragment_summary
                )
            )
            

            print(
                "PEAK SUMMARY =",
                peak_summary
            )

            memory_metrics["peak_memory_gb"] = (
                peak_summary.get("peak_memory_gb", 0)
            )

            memory_metrics["peak_memory_mb"] = round(
                peak_summary.get("peak_memory_gb", 0) * 1024,
                2
            )

            memory_metrics["components"] = (
                peak_summary.get("components", [])
            )

        exec_summary = ExecSummaryExtractor().parse(text)
        operator_metrics = OperatorExtractor().parse(text)
        network_metrics = NetworkExtractor().parse(text)
        cpu_metrics = CPUExtractor().parse(text)

        sanitized_timeline = sanitize_timeline(timeline)

        profile = QueryProfile(
            query_info=query_info,
            timeline=sanitized_timeline,
            metadata=metadata,
            exec_summary=exec_summary,
            fragment_instances=fragment_instances,
            scan_metrics=scan_metrics,
            resource_metrics=resource_metrics,
            memory_metrics=memory_metrics,
            operator_metrics=operator_metrics,
            cpu_metrics=cpu_metrics,
            network_metrics=network_metrics,
            raw_profile=text
        )

        print("=" * 80)
        print("QUERY ID:", query_info.query_id)
        print("Fragments extracted:", len(fragment_instances))
        print("=" * 80)

        return profile

