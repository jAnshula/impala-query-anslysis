from analyzers.findings import Finding

class ScanAnalyzer:

    def analyze(self, scan):

        findings = []

        rows = scan.get(
            "rows_read",
            0
        )

        files = scan.get(
            "files_scanned",
            0
        )

        partitions = scan.get(
            "partitions_scanned",
            0
        )

        if partitions > 300:

            findings.append(
                Finding(
                    category="scan",
                    severity="HIGH",
                    title="Excessive Partition Scan",
                    description=(
                        f"{partitions} partitions scanned."
                    ),
                    evidence=scan,
                    impact_score=80
                )
            )

        if files > 500:

            findings.append(
                Finding(
                    category="scan",
                    severity="HIGH",
                    title="Small Files Problem",
                    description=(
                        f"{files} files scanned."
                    ),
                    evidence=scan,
                    impact_score=85
                )
            )

        if rows > 1_000_000_000:

            findings.append(
                Finding(
                    category="scan",
                    severity="MEDIUM",
                    title="Large Scan Volume",
                    description=(
                        f"{rows:,} rows scanned."
                    ),
                    evidence=scan,
                    impact_score=60
                )
            )

        return findings

