from statistics import mean
from analyzers.findings import Finding

class FragmentAnalyzer:

    def analyze(self, fragments):

        findings = []

        if not fragments:
            return findings

        runtimes = [
            x.runtime_ms
            for x in fragments
            if x.runtime_ms > 0
        ]

        if len(runtimes) < 2:
            return findings

        avg_runtime = mean(runtimes)

        max_runtime = max(runtimes)

        skew_ratio = max_runtime / avg_runtime

        if skew_ratio > 3:

            findings.append(
                Finding(
                    category="execution",
                    severity="CRITICAL",
                    title="Fragment Runtime Skew",
                    description=(
                        f"Max runtime is "
                        f"{skew_ratio:.1f}x "
                        f"higher than average."
                    ),
                    evidence={
                        "avg_runtime":
                            avg_runtime,
                        "max_runtime":
                            max_runtime
                    },
                    impact_score=95
                )
            )

        return findings

