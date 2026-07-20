class RootCauseSummaryAnalyzer:

    def analyze(
        self,
        profile,
        runtime_breakdown
    ):

        findings = []

        text = getattr(
            profile,
            "raw_profile",
            ""
        )

        planning_pct = (
            runtime_breakdown.get(
                "planning_pct",
                0
            )
        )

        if (
            planning_pct > 80
            and (
                "PARTITION_NOT_FOUND" in text
                or
                "inconsistent metadata" in text
            )
        ):

            findings.append({

                "category":
                    "metadata",

                "severity":
                    "critical",

                "title":
                    "Catalog Metadata Inconsistency",

                "description":
                    (
                        f"Planning consumed "
                        f"{planning_pct:.1f}% "
                        f"of runtime because "
                        f"metadata was inconsistent."
                    )
            })

        return findings

