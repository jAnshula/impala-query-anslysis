from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ExecSummaryOperator:
    """
    Represents a single operator row from the Impala ExecSummary.
    """

    operator_id: int

    operator_type: str

    fragment_id: str

    avg_time_ms: int = 0

    max_time_ms: int = 0

    rows_produced: int = 0

    peak_memory_bytes: int = 0

    est_peak_memory_bytes: int = 0

    @property
    def peak_memory_mb(self) -> float:
        return round(
            self.peak_memory_bytes /
            (1024 * 1024),
            2
        )

    @property
    def est_peak_memory_mb(self) -> float:
        return round(
            self.est_peak_memory_bytes /
            (1024 * 1024),
            2
        )

    def to_dict(self):

        return {
            "operator_id": self.operator_id,
            "operator_type": self.operator_type,
            "fragment_id": self.fragment_id,
            "avg_time_ms": self.avg_time_ms,
            "max_time_ms": self.max_time_ms,
            "rows_produced": self.rows_produced,
            "peak_memory_bytes":
                self.peak_memory_bytes,
            "est_peak_memory_bytes":
                self.est_peak_memory_bytes,
            "peak_memory_mb":
                self.peak_memory_mb,
            "est_peak_memory_mb":
                self.est_peak_memory_mb
        }


@dataclass
class ExecSummaryFragment:
    """
    Represents a fragment section in ExecSummary.
    """

    fragment_id: str

    operators: List[
        ExecSummaryOperator
    ] = field(
        default_factory=list
    )

    host_count: int = 0

    instance_count: int = 0

    @property
    def operator_count(self) -> int:

        return len(
            self.operators
        )

    @property
    def total_rows(self) -> int:

        return sum(
            op.rows_produced
            for op in self.operators
        )

    @property
    def max_operator_time_ms(self) -> int:

        if not self.operators:
            return 0

        return max(
            op.max_time_ms
            for op in self.operators
        )

    @property
    def total_peak_memory_bytes(self) -> int:

        return sum(
            op.peak_memory_bytes
            for op in self.operators
        )

    @property
    def total_peak_memory_mb(self) -> float:

        return round(
            self.total_peak_memory_bytes /
            (1024 * 1024),
            2
        )

    def to_dict(self):

        return {
            "fragment_id":
                self.fragment_id,

            "host_count":
                self.host_count,

            "instance_count":
                self.instance_count,

            "operator_count":
                self.operator_count,

            "total_rows":
                self.total_rows,

            "max_operator_time_ms":
                self.max_operator_time_ms,

            "total_peak_memory_mb":
                self.total_peak_memory_mb
        }


@dataclass
class ExecSummary:
    """
    Top-level ExecSummary container.
    """

    fragments: List[
        ExecSummaryFragment
    ] = field(
        default_factory=list
    )

    @property
    def fragment_count(self) -> int:

        return len(
            self.fragments
        )

    @property
    def total_hosts(self) -> int:

        return sum(
            fragment.host_count
            for fragment in self.fragments
        )

    @property
    def total_instances(self) -> int:

        return sum(
            fragment.instance_count
            for fragment in self.fragments
        )

    def get_fragment(
        self,
        fragment_id: str
    ) -> Optional[
        ExecSummaryFragment
    ]:

        fragment_id = (
            str(fragment_id)
            .strip()
            .upper()
        )

        for fragment in self.fragments:

            if (
                fragment.fragment_id
                .upper()
                == fragment_id
            ):
                return fragment

        return None

    def to_dict(self):

        return {
            "fragment_count":
                self.fragment_count,

            "total_hosts":
                self.total_hosts,

            "total_instances":
                self.total_instances,

            "fragments": [
                fragment.to_dict()
                for fragment
                in self.fragments
            ]
        }

