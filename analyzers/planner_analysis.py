import re


class PlannerAnalyzer:

    def analyze(self, profile):

        findings = []

        timeline = getattr(
            profile,
            "timeline", None
        )

        if not timeline:
            return findings

        planning = timeline.get(
            "planning_ms",
            0
        )

        admission = timeline.get(
            "admission_ms",
            0
        )

        execution = timeline.get(
            "execution_ms",
            0
        )

        total = (
            planning +
            admission +
            execution
        )

        if total <= 0:
            return findings

        planning_pct = (
            planning * 100
        ) / total

        if (
            planning > 60000
            or planning_pct > 30
        ):

            findings.append(
                {
                    "category":
                        "planning",

                    "severity":
                        "critical",

                    "title":
                        "Frontend Planning Bottleneck",

                    "description":
                        (
                            f"Planning consumed "
                            f"{planning_pct:.1f}% "
                            f"of total runtime."
                        )
                }
            )

        profile_text = getattr(
            profile,
            "raw_profile",
            ""
        )

        retry_match = re.search(
            r"Retried query planning due to inconsistent metadata\s+(\d+)",
            profile_text,
            re.IGNORECASE
        )

        if retry_match:

            retries = int(
                retry_match.group(1)
            )

            findings.append(
                {
                    "category":
                        "metadata",

                    "severity":
                        "critical",

                    "title":
                        "Metadata Inconsistency During Planning",

                    "description":
                        (
                            f"Planner retried "
                            f"{retries} times due to "
                            f"inconsistent metadata."
                        )
                }
            )

        return findings

