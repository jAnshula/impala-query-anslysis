class AdmissionAnalyzer:

    def analyze(self, timeline):

        findings = []

        admission_ms = timeline.get(
            "admission_ms",
            0
        )

        if admission_ms > 30000:

            findings.append(
                {
                    "category":
                        "admission",

                    "severity":
                        "high",

                    "title":
                        "Admission Queue Delay",

                    "description":
                        (
                            f"Query spent "
                            f"{admission_ms/1000:.1f}s "
                            f"waiting for admission."
                        )
                }
            )

        return findings

