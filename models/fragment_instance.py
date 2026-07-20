from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FragmentInstance:
    """Represents a single Impala fragment instance execution.
    
    Captures metrics for a specific fragment instance running on a host,
    including runtime, memory usage, I/O, and network statistics.
    """

    # Identity
    query_id: str = ""
    """Query this fragment belongs to"""

    fragment: str = ""
    """Fragment identifier"""

    instance_id: str = ""
    """Instance identifier within fragment"""

    host: str = ""
    """Host where fragment executed"""

    operator: str = ""
    """Operator type (SCAN, HASH_JOIN, etc.)"""

    # Runtime
    runtime_ms: int = 0
    """Fragment execution time in milliseconds"""

    rows: int = 0
    """Rows produced by this fragment"""

    # IO
    read_bytes: int = 0
    """Bytes read from storage"""

    write_bytes: int = 0
    """Bytes written"""

    io_wait_ms: int = 0
    """Time spent waiting on I/O operations"""

    # Memory
    peak_memory: int = 0
    """Peak memory usage in bytes"""

    # Network
    network_send_ms: int = 0
    """Time spent sending data over network"""

    network_receive_ms: int = 0
    """Time spent receiving data over network"""

    @property
    def total_network_ms(self) -> int:
        """Total network I/O time (send + receive)."""
        return (
            self.network_send_ms
            + self.network_receive_ms
        )

    @property
    def read_mb(self) -> float:
        """Bytes read converted to MB."""
        return round(
            self.read_bytes / (1024 * 1024),
            2
        )

    @property
    def write_mb(self) -> float:
        """Bytes written converted to MB."""
        return round(
            self.write_bytes / (1024 * 1024),
            2
        )

    @property
    def peak_memory_mb(self) -> float:
        """Peak memory converted to MB."""
        return round(
            self.peak_memory / (1024 * 1024),
            2
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert fragment instance to dictionary representation."""
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