# analyzers/query_health.py

class QueryHealthAnalyzer:

    def calculate_score(self, findings, metrics=None):

        score = 100

        for f in findings:

            severity = (
                getattr(
                    f,
                    "severity",
                    None
                )
                or f.get(
                    "severity",
                    ""
                )
            ).lower()

            if severity == "critical":
                score -= 30
            elif severity == "high":
                score -= 20
            elif severity == "medium":
                score -= 10
            elif severity == "low":
                score -= 5

        metrics = metrics or {}

        bytes_read = metrics.get("bytes_read", 0)

        tb = bytes_read / (1024 ** 4)

        if tb > 10:
            score -= 30
        elif tb > 5:
            score -= 20
        elif tb > 1:
            score -= 10

        runtime_ms = metrics.get("runtime_ms", 0)

        if runtime_ms > 1800000:
            score -= 40
        elif runtime_ms > 900000:
            score -= 25
        elif runtime_ms > 300000:
            score -= 10

        return max(min(score, 100), 0)

