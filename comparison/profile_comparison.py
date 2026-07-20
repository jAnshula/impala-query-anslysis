from dataclasses import dataclass

@dataclass
class ComparisonResult:

    duration_delta_pct: float

    planning_delta_pct: float

    memory_delta_pct: float

    admission_delta_pct: float

class ProfileComparison:

    def compare(
        self,
        current,
        baseline
    ):

        return ComparisonResult(

            duration_delta_pct=
                self._pct_change(
                    baseline.duration_ms,
                    current.duration_ms
                ),

            planning_delta_pct=
                self._pct_change(
                    baseline.timeline.planning_ms,
                    current.timeline.planning_ms
                ),

            memory_delta_pct=
                self._pct_change(
                    baseline.resource_usage.peak_memory_bytes,
                    current.resource_usage.peak_memory_bytes
                ),

            admission_delta_pct=
                self._pct_change(
                    baseline.timeline.admission_ms,
                    current.timeline.admission_ms
                )
        )

    def _pct_change(
        self,
        old,
        new
    ):

        if old == 0:
            return 0

        return (
            (new - old) / old
        ) * 100

