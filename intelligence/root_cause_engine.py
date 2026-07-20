from intelligence.root_cause import RootCause


class RootCauseEngine:

    ROOT_CAUSE_MAP = {

        "planning": {
            "id": "planning_delay",
            "confidence": 0.95,
            "impact": 90,
            "recommendations": [
                "catalog_health",
                "compute_stats"
            ]
        },

        "scan": {
            "id": "large_scan",
            "confidence": 0.95,
            "impact": 95,
            "recommendations": [
                "partition_pruning",
                "predicate_pushdown",
                "file_compaction"
            ]
        },

        "execution": {
            "id": "fragment_skew",
            "confidence": 0.90,
            "impact": 85,
            "recommendations": [
                "data_distribution",
                "join_strategy"
            ]
        },

        "statistics": {
            "id": "missing_statistics",
            "confidence": 0.90,
            "impact": 75,
            "recommendations": [
                "compute_stats"
            ]
        },

        "admission": {
            "id": "admission_delay",
            "confidence": 0.95,
            "impact": 90,
            "recommendations": [
                "increase_pool_capacity"
            ]
        },

        "metadata": {
            "id": "metadata_delay",
            "confidence": 0.95,
            "impact": 95,
            "recommendations": [
                "refresh_metadata",
                "catalog_health",
                "review_partitions"
            ]
        },

        "failure": {
            "id": "query_failure",
            "confidence": 1.0,
            "impact": 100,
            "recommendations": []
        },

        "memory": {
            "id": "memory_spill",
            "confidence": 0.95,
            "impact": 90,
            "recommendations": [
                "increase_mem_limit"
            ]
        },
    }

    def analyze(self, findings):
        cause_map = {}

        for finding in findings:

            if isinstance(finding, dict):

                category = finding.get(
                    "category",
                    ""
                )

                title = finding.get(
                    "title",
                    ""
                )

                description = finding.get(
                    "description",
                    ""
                )

                severity = finding.get(
                    "severity",
                    "medium"
                ).upper()

            else:

                category = getattr(
                    finding,
                    "category",
                    ""
                )

                title = getattr(
                    finding,
                    "title",
                    ""
                )

                description = getattr(
                    finding,
                    "description",
                    ""
                )

                severity = getattr(
                    finding,
                    "severity",
                    "medium"
                ).upper()

            #
            # Memory Special Handling
            #
            if category == "memory":

                title_lower = title.lower()

                if "spill" in title_lower:

                    root_cause_id = "memory_spill"

                    if root_cause_id not in cause_map:

                        cause_map[root_cause_id] = RootCause(
                            id="memory_spill",
                            title="Memory Spill",
                            severity=severity,
                            confidence=0.95,
                            impact_score=90,
                            evidence=[],
                            recommendation_ids=[
                                "increase_mem_limit"
                            ]
                        )

                    if description:
                        cause_map[
                            root_cause_id
                        ].evidence.append(
                            description
                        )

                else:

                    root_cause_id = "memory_pressure"

                    if root_cause_id not in cause_map:

                        cause_map[root_cause_id] = RootCause(
                            id="memory_pressure",
                            title="Memory Pressure",
                            severity=severity,
                            confidence=0.95,
                            impact_score=95,
                            evidence=[],
                            recommendation_ids=[
                                "increase_mem_limit"
                            ]
                        )

                    if description:
                        cause_map[
                            root_cause_id
                        ].evidence.append(
                            description
                        )

                continue

            config = self.ROOT_CAUSE_MAP.get(
                category
            )

            if not config:
                continue

            root_cause_id = config["id"]

            #
            # First occurrence creates root cause
            #
            if root_cause_id not in cause_map:

                cause_map[root_cause_id] = RootCause(
                    id=root_cause_id,
                    title=title,
                    severity=severity,
                    confidence=config[
                        "confidence"
                    ],
                    impact_score=config[
                        "impact"
                    ],
                    evidence=[],
                    recommendation_ids=config[
                        "recommendations"
                    ]
                )

            #
            # Subsequent findings contribute evidence
            #
            if description:

                if (
                    description
                    not in
                    cause_map[
                        root_cause_id
                    ].evidence
                ):

                    cause_map[
                        root_cause_id
                    ].evidence.append(
                        description
                    )

        return sorted(
            list(
                cause_map.values()
            ),
            key=lambda x: x.impact_score,
            reverse=True
        )

