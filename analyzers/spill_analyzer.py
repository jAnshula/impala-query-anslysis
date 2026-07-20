from analyzers.findings import Finding

class SpillAnalyzer:

    def analyze(self, memory_metrics):

        findings = []

        if not memory_metrics:
            return findings

        if memory_metrics.get("spill_detected"):

            findings.append(
                Finding(
                    category="memory",
                    severity="HIGH",
                    title="Disk Spill Detected",
                    description=(
                        f"Query spilled to disk. "
                        f"Spill count = "
                        f"{memory_metrics.get('spill_count',0)}"
                    ),
                    evidence=memory_metrics,
                    impact_score=85
                )
            )

        return findings

