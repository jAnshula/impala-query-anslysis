from analyzers.query_health import QueryHealthAnalyzer
from analyzers.failure_analyzer import FailureAnalyzer
from analyzers.admission_analyzer import AdmissionAnalyzer
from analyzers.metadata_analyzer import MetadataAnalyzer
from analyzers.statistics_analyzer import StatisticsAnalyzer
from analyzers.runtime_breakdown_analyzer import (
    RuntimeBreakdownAnalyzer
)

class AnalyticsEngine:

    def analyze(self, profile):

        findings = []
        root_causes = []

        # ----------------------------------
        # Fragment Runtime Analysis
        # ----------------------------------

        instances = getattr(
            profile,
            "fragment_instances",
            []
        )

        runtimes = []

        total_runtime_ms = 0

        skew_pct = 0

        for instance in instances:

            runtime = getattr(
                instance,
                "runtime_ms",
                0
            )

            if runtime > 0:

                runtimes.append(runtime)

                total_runtime_ms += runtime

        # ----------------------------------
        # Runtime Skew Detection
        # ----------------------------------

        if runtimes:

            avg_runtime = (
                sum(runtimes)
                / len(runtimes)
            )

            max_runtime = max(
                runtimes
            )

            if avg_runtime > 0:

                skew_pct = (
                    (
                        max_runtime
                        - avg_runtime
                    )
                    /
                    avg_runtime
                ) * 100

                if skew_pct > 100:

                    findings.append(
                        {
                            "category":
                                "execution",

                            "severity":
                                "high",

                            "title":
                                "Fragment Runtime Skew",

                            "description":
                                (
                                    f"Max runtime "
                                    f"{max_runtime/1000:.1f}s "
                                    f"vs average "
                                    f"{avg_runtime/1000:.1f}s. "
                                    f"Slowest fragment is "
                                    f"{skew_pct:.0f}% slower "
                                    f"than average."
                                )
                        }
                    )

        if skew_pct > 300:

            findings.append(
                {
                    "category":
                        "execution",

                    "severity":
                        "critical",

                    "title":
                        "Severe Fragment Runtime Skew",

                    "description":
                        (
                            f"Slowest fragment is "
                            f"{skew_pct:.0f}% slower "
                            f"than average."
                        )
                }
            )

        # ----------------------------------
        # Peak Memory Analysis
        # ----------------------------------

        peak_memory = (
            profile.memory_metrics.get(
                "peak_memory_gb",
                0
            )
        )

        if peak_memory > 50:

            findings.append(
                {
                    "category":
                        "memory",

                    "severity":
                        "critical",

                    "title":
                        "Extreme Memory Consumption",

                    "description":
                        (
                            f"Peak memory reached "
                            f"{peak_memory:.1f} GB."
                        )
                }
            )

        # ----------------------------------
        # Scan Metrics
        # ----------------------------------

        scan_metrics = getattr(
            profile,
            "scan_metrics",
            {}
        ) or {}

        resource_metrics = getattr(
            profile,
            "resource_metrics",
            {}
        ) or {}

        memory_metrics = getattr(
            profile,
            "memory_metrics",
            {}
        ) or {}

        files_scanned = (
            scan_metrics.get(
                "files_scanned",
                0
            )
        )

        if files_scanned > 500:

            findings.append(
                {
                    "category":
                        "scan",

                    "severity":
                        "high",

                    "title":
                        "Large File Scan",

                    "description":
                        f"{files_scanned} files scanned."
                }
            )

        # ----------------------------------
        # Large Scan Detection
        # ----------------------------------

        bytes_read = scan_metrics.get(
            "bytes_read",
            0
        )

        if bytes_read > 5 * 1024**4:

            findings.append(
                {
                    "category":
                        "scan",

                    "severity":
                        "critical",

                    "title":
                        "Massive Scan Volume",

                    "description":
                        (
                            f"Scanned "
                            f"{bytes_read / 1024**4:.2f} TB"
                        )
                }
            )

        if files_scanned > 50000:

            findings.append(
                {
                    "category":
                        "scan",

                    "severity":
                        "high",

                    "title":
                        "Excessive File Count",

                    "description":
                        (
                            f"Scanned "
                            f"{files_scanned:,} files"
                        )
                }
            )

        # ----------------------------------
        # Spill Detection
        # ----------------------------------

        spill_detected = memory_metrics.get(
            "spill_detected",
            False
        )

        spill_count = memory_metrics.get(
            "spill_count",
            0
        )

        if spill_detected:

            severity = (
                "critical"
                if spill_count > 20
                else "high"
            )

            findings.append(
                {
                    "category":
                        "memory",

                    "severity":
                        severity,

                    "title":
                        "Memory Spill Detected",

                    "description":
                        (
                            f"{spill_count} spill events "
                            f"detected. Operators spilled "
                            f"to disk which can significantly "
                            f"impact query performance."
                        ),

                    "evidence":
                        memory_metrics
                }
            )

        # ----------------------------------
        # Timeline Analysis
        # ----------------------------------

        timeline = getattr(
            profile,
            "timeline",
            {}
        ) or {}

        findings.extend(
            FailureAnalyzer()
            .analyze(profile)
        )

        findings.extend(
            AdmissionAnalyzer()
            .analyze(timeline)
        )

        findings.extend(
            MetadataAnalyzer()
            .analyze(timeline)
        )

        # ----------------------------------
        # Runtime Breakdown
        # ----------------------------------

        runtime_breakdown = (
            RuntimeBreakdownAnalyzer()
            .analyze(profile)
        )

        planning_pct = (
            runtime_breakdown.get(
                "planning_pct",
                0
            )
        )

        if planning_pct > 80:

            findings.append(
                {
                    "category":
                        "planning",

                    "severity":
                        "critical",

                    "title":
                        "Planning Dominates Runtime",

                    "description":
                        (
                            f"Planning consumed "
                            f"{planning_pct:.1f}% "
                            f"of total runtime."
                        )
                }
            )

        # ----------------------------------
        # Metadata Retry Detection
        # ----------------------------------

        profile_text = getattr(
            profile,
            "raw_profile",
            ""
        )

        if (
            "PARTITION_NOT_FOUND"
            in profile_text
        ):

            findings.append(
                {
                    "category":
                        "metadata",

                    "severity":
                        "critical",

                    "title":
                        "Catalog Metadata Inconsistency",

                    "description":
                        (
                            "PARTITION_NOT_FOUND "
                            "encountered during planning."
                        )
                }
            )

        if (
            "Retried query planning due to inconsistent metadata"
            in profile_text
        ):

            findings.append(
                {
                    "category":
                        "metadata",

                    "severity":
                        "critical",

                    "title":
                        "Metadata Retry Detected",

                    "description":
                        (
                            "Planning retried because of "
                            "catalog metadata inconsistency."
                        )
                }
            )

            if not any(
                rc["title"] ==
                "Catalog Metadata Inconsistency"
                for rc in root_causes
            ):

                root_causes.append(
                    {
                        "title":
                            "Catalog Metadata Inconsistency",

                        "severity":
                            "critical",

                        "description":
                            (
                                "Catalog metadata inconsistency "
                                "caused repeated planning retries."
                            )
                    }
                )

        # ----------------------------------
        # Statistics Analysis
        # ----------------------------------

        statistics = {}

        if profile.metadata.get(
            "compute_stats_missing",
            False
        ):

            statistics[
                "missing_stats"
            ] = True

        findings.extend(
            StatisticsAnalyzer()
            .analyze(statistics)
        )

        # ----------------------------------
        # Metrics
        # ----------------------------------

        metrics = {}

        metrics.update(
            scan_metrics
        )

        metrics.update(
            resource_metrics
        )

        metrics["runtime_ms"] = (
            total_runtime_ms
        )

        # ----------------------------------
        # Score
        # ----------------------------------

        score = (
            QueryHealthAnalyzer()
            .calculate_score(
                findings,
                metrics
            )
        )


        return {

            "health_score":
                score,

            "findings":
                findings,

            "root_causes":
                root_causes,

            "runtime_breakdown":
                runtime_breakdown
        }