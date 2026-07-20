import re

class PlanningRetryAnalyzer:

    def analyze(self, profile):

        findings = []

        text = getattr(
            profile,
            "raw_profile",
            ""
        )

        m = re.search(
            r"Retried query planning due to inconsistent metadata\s+(\d+)",
            text
        )

        if not m:
            return findings

        retries = int(
            m.group(1)
        )

        if retries > 5:

            findings.append({

                "category":
                    "metadata",

                "severity":
                    "critical",

                "title":
                    "Excessive Planning Retries",

                "description":
                    f"Planning retried "
                    f"{retries} times."
            })

        return findings

