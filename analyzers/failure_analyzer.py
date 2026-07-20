import re

class FailureAnalyzer:

    def analyze(self, profile):

        findings = []

        text = getattr(
            profile,
            "raw_profile",
            ""
        ).lower()

        checks = [

            (
                r"memory limit exceeded",
                "Memory Limit Exceeded",
                "memory"
            ),

            (
                r"query cancelled|cancelled due to",
                "Query Cancelled",
                "failure"
            ),

            (
                r"rpc.*(failed|timeout|timed out|error)",
                "RPC Failure",
                "network"
            ),

            (
                r"disk io error|i/o error|filesystem error",
                "Disk I/O Failure",
                "storage"
            )
        ]

        for pattern, title, category in checks:

            if re.search(pattern, text):

                findings.append({
                    "category": category,
                    "severity": "critical",
                    "title": title,
                    "description":
                        f"Detected {title} in query profile."
                })

        return findings

