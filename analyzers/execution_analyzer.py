from collections import defaultdict
from core.time_util import ms_to_hms

def bytes_to_mb(b):
    return round(b / (1024 * 1024), 2)

def bytes_to_gb(b):
    return round(b / (1024 * 1024 * 1024), 2)

class ExecutionAnalyzer:

    def fragment_summary(self, instances):
        result = defaultdict(
            lambda: {
                "instances": 0,
                "runtime_ms": 0,
                "avg_runtime_ms": 0,
                "rows": 0,
                "read_bytes": 0,
                "write_bytes": 0,
                "read_mb": 0.0,
                "write_mb": 0.0,
                "peak_memory": 0,
                "peak_memory_mb": 0.0,
                "peak_memory_gb": 0.0,
                "network_send_ms": 0,
                "network_receive_ms": 0,
                "network_ms": 0,
                "io_wait_ms": 0
            }
        )

        for i in instances:
            fragment = i.fragment or "UNKNOWN"
            f = result[fragment]

            f["instances"] += 1
            f["runtime_ms"] += i.runtime_ms
            f["rows"] += i.rows
            f["read_bytes"] += i.read_bytes
            f["write_bytes"] += i.write_bytes
            f["network_send_ms"] += i.network_send_ms
            f["network_receive_ms"] += i.network_receive_ms
            f["network_ms"] += i.network_send_ms + i.network_receive_ms
            f["io_wait_ms"] += i.io_wait_ms

            # Track peak memory
            f["peak_memory"] = max(f["peak_memory"], i.peak_memory)

        # Derived metrics
        for fragment in result.values():
            instances_count = fragment["instances"]

            if instances_count > 0:
                fragment["avg_runtime_ms"] = round(
                    fragment["runtime_ms"] / instances_count, 2
                )

            fragment["read_mb"] = bytes_to_mb(fragment["read_bytes"])
            fragment["write_mb"] = bytes_to_mb(fragment["write_bytes"])
            fragment["peak_memory_mb"] = bytes_to_mb(fragment["peak_memory"])
            fragment["peak_memory_gb"] = bytes_to_gb(fragment["peak_memory"])

            fragment["runtime_hms"] = ms_to_hms(fragment["runtime_ms"])
            fragment["avg_runtime_hms"] = ms_to_hms(fragment["avg_runtime_ms"])

        return dict(result)
    
    def peak_memory_summary(self, fragment_summary):
        """Return overall peak memory across all fragments in GB,
        plus a breakdown of components for memory_breakdown UI."""
        if not fragment_summary:
            return {
                "peak_memory_gb": 0.0,
                "components": []
            }

        max_peak = max(
        (f["peak_memory"] for f in fragment_summary.values()),
        default=0
        )


        # Build component breakdown for UI
        components = []
        for frag_name, frag in fragment_summary.items():
            components.append({
                "Fragment": frag_name,
                "Peak Memory (MB)": round(frag["peak_memory_mb"], 2),
                "Peak Memory (GB)": round(frag["peak_memory_gb"], 2),
                "Instances": frag["instances"],
                "Runtime (HH:MM:SS)": frag.get("runtime_hms", "00:00:00")
            })

        return {
            "peak_memory_gb": bytes_to_gb(max_peak),
            "components": components
        }


    def top_slowest_fragments(self, fragment_summary, limit=5):
        return sorted(
            fragment_summary.items(),
            key=lambda x: x[1]["runtime_ms"],
            reverse=True
        )[:limit]

    def top_network_fragments(self, fragment_summary, limit=5):
        return sorted(
            fragment_summary.items(),
            key=lambda x: x[1]["network_ms"],
            reverse=True
        )[:limit]

    def top_io_fragments(self, fragment_summary, limit=5):
        return sorted(
            fragment_summary.items(),
            key=lambda x: x[1]["io_wait_ms"],
            reverse=True
        )[:limit]

