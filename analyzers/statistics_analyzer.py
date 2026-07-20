from analyzers.findings import Finding


class StatisticsAnalyzer:

    def analyze(self, statistics):

        findings = []

        #
        # Missing table stats
        #
        if statistics.get("missing_stats"):

            findings.append(
                Finding(
                    category="statistics",
                    severity="HIGH",
                    title="Missing Table Statistics",
                    description=(
                        "Optimizer is operating "
                        "without table statistics."
                    ),
                    evidence=statistics,
                    impact_score=80
                )
            )

        #
        # Missing column stats
        #
        if statistics.get("missing_column_stats"):

            findings.append(
                Finding(
                    category="statistics",
                    severity="MEDIUM",
                    title="Missing Column Statistics",
                    description=(
                        "Cardinality estimation may "
                        "be inaccurate."
                    ),
                    evidence=statistics,
                    impact_score=60
                )
            )

        #
        # Corrupt / suspicious stats
        #
        if statistics.get("corrupt_stats"):

            findings.append(
                Finding(
                    category="statistics",
                    severity="CRITICAL",
                    title="Corrupt Statistics Detected",
                    description=(
                        "Statistics appear inconsistent "
                        "with actual data volume and may "
                        "cause incorrect optimizer decisions."
                    ),
                    evidence=statistics,
                    impact_score=95
                )
            )

        #
        # Stale stats
        #
        if statistics.get("stale_stats"):

            findings.append(
                Finding(
                    category="statistics",
                    severity="HIGH",
                    title="Stale Statistics",
                    description=(
                        "Statistics may no longer reflect "
                        "current table contents."
                    ),
                    evidence=statistics,
                    impact_score=75
                )
            )

        return findings

