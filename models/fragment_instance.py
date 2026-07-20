from dataclasses import dataclass


@dataclass
class FragmentInstance:
    """
    Represents a single Impala fragment instance execution.
    """

    #
    # Identity
    #
    query_id: str = ""

    fragment: str = ""

    instance_id: str = ""

    host: str = ""

    operator: str = ""

    #
    # Runtime
    #
    runtime_ms: int = 0

    rows: int = 0

    #
    # IO
    #
    read_bytes: int = 0

    write_bytes: int = 0

    io_wait_ms: int = 0

    #
    # Memory
    #
    peak_memory: int = 0

    #
    # Network
    #
    network_send_ms: int = 0

    network_receive_ms: int = 0

    @property
    def total_network_ms(self) -> int:
        return (
            self.network_send_ms
            + self.network_receive_ms
        )

    @property
    def read_mb(self) -> float:
        return round(
            self.read_bytes / (1024 * 1024),
            2
        )

    @property
    def write_mb(self) -> float:
        return round(
            self.write_bytes / (1024 * 1024),
            2
        )

    @property
    def peak_memory_mb(self) -> float:
        return round(
            self.peak_memory / (1024 * 1024),
            2
        )

    def to_dict(self):

        return {
            "query_id": self.query_id,
            "fragment": self.fragment,
            "instance_id": self.instance_id,
            "host": self.host,
            "operator": self.operator,
            "runtime_ms": self.runtime_ms,
            "rows": self.rows,
            "read_bytes": self.read_bytes,
            "write_bytes": self.write_bytes,
            "read_mb": self.read_mb,
            "write_mb": self.write_mb,
            "peak_memory": self.peak_memory,
            "peak_memory_mb": self.peak_memory_mb,
            "network_send_ms": self.network_send_ms,
            "network_receive_ms": self.network_receive_ms,
            "total_network_ms": self.total_network_ms,
            "io_wait_ms": self.io_wait_ms
        }

