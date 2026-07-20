class TrendAnalyzer:

    def analyze(
        self,
        historical_profiles
    ):

        return {

            "avg_runtime":

                sum(
                    p.duration_ms
                    for p in historical_profiles
                )
                / len(historical_profiles),

            "avg_health_score":

                sum(
                    p.health_score
                    for p in historical_profiles
                )
                / len(historical_profiles)
        }

