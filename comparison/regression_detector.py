class RegressionDetector:

    def detect(
        self,
        comparison
    ):

        regressions = []

        if comparison.duration_delta_pct > 50:

            regressions.append(
                "Execution time increased "
                "more than 50%"
            )

        if comparison.memory_delta_pct > 100:

            regressions.append(
                "Memory doubled"
            )

        if comparison.planning_delta_pct > 100:

            regressions.append(
                "Planning regression detected"
            )

        return regressions

