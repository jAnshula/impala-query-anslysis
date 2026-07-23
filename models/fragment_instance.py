from dataclasses import dataclass, field

@dataclass
class FragmentInstance:
    """Standardized fragment instance with all metrics."""
    
    query_id: str = ""
    fragment: str = "F0"
    instance_id: str = ""
    host: str = "UNKNOWN"
    operator: str = "UNKNOWN"
    
    # Runtime metrics (in milliseconds)
    runtime_ms: int = 0
    
    # Row metrics
    rows: int = 0
    
    # I/O metrics (in bytes)
    read_bytes: int = 0
    write_bytes: int = 0
    spill_bytes: int = 0
    bytes_sent: int = 0
    
    # Memory metrics (in bytes)
    peak_memory: int = 0
    
    # Wait metrics (in milliseconds)
    io_wait_ms: int = 0
    network_send_ms: int = 0
    network_receive_ms: int = 0
    scanner_time_ms: int = 0
    scanner_threads: int = 0
    
    @property
    def read_mb(self) -> float:
        return round(self.read_bytes / (1024**2), 2)
    
    @property
    def write_mb(self) -> float:
        return round(self.write_bytes / (1024**2), 2)
    
    @property
    def peak_memory_mb(self) -> float:
        return round(self.peak_memory / (1024**2), 2)
    
    @property
    def peak_memory_gb(self) -> float:
        return round(self.peak_memory / (1024**3), 2)
    
    @property
    def total_network_ms(self) -> int:
        return self.network_send_ms + self.network_receive_ms
    
    def to_dict(self) -> dict:
        return {
            "query_id": self.query_id,
            "fragment": self.fragment,
            "instance_id": self.instance_id,
            "host": self.host,
            "operator": self.operator,
            "runtime_ms": self.runtime_ms,
            "rows": self.rows,
            "read_mb": self.read_mb,
            "write_mb": self.write_mb,
            "peak_memory_mb": self.peak_memory_mb,
            "peak_memory_gb": self.peak_memory_gb,
            "io_wait_ms": self.io_wait_ms,
            "total_network_ms": self.total_network_ms,
            "scanner_time_ms": self.scanner_time_ms,
        }