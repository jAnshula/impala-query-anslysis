from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FragmentInstance:
    """Represents a single Impala fragment instance execution."""

    # Identity
    query_id: str = ""
    fragment: str = ""
    instance_id: str = ""
    host: str = ""
    operator: str = ""

    # Runtime
    runtime_ms: int = 0
    rows: int = 0

    # IO
    read_bytes: int = 0
    write_bytes: int = 0
    io_wait_ms: int = 0

    # Memory
    peak_memory: int = 0
    spill_bytes: int = 0   # NEW

    # Network
    network_send_ms: int = 0
    network_receive_ms: int = 0
    bytes_sent: int = 0    # NEW

    # Scanner
    scanner_time_ms: int = 0   # NEW
    scanner_threads: int = 0   # NEW

    @property
    def total_network_ms(self) -> int:
        return self.network_send_ms + self.network_receive_ms

    @property
    def read_mb(self) -> float:
        return round(self.read_bytes / (1024 * 1024), 2)

    @property
    def write_mb(self) -> float:
        return round(self.write_bytes / (1024 * 1024), 2)

    @property
    def peak_memory_mb(self) -> float:
        return round(self.peak_memory / (1024 * 1024), 2)

    @property
    def spill_mb(self) -> float:
        return round(self.spill_bytes / (1024 * 1024), 2)

    @property
    def sent_mb(self) -> float:
        return round(self.bytes_sent / (1024 * 1024), 2)

    def to_dict(self) -> Dict[str, Any]:
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
            "spill_bytes": self.spill_bytes,
            "spill_mb": self.spill_mb,
            "network_send_ms": self.network_send_ms,
            "network_receive_ms": self.network_receive_ms,
            "total_network_ms": self.total_network_ms,
            "bytes_sent": self.bytes_sent,
            "sent_mb": self.sent_mb,
            "scanner_time_ms": self.scanner_time_ms,
            "scanner_threads": self.scanner_threads,
            "io_wait_ms": self.io_wait_ms,
        }
