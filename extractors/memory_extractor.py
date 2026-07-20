import re


class MemoryExtractor:

    def parse(self, text):

        result = {
            "cluster_memory_admitted_gb": 0.0,
            "per_host_memory_estimate_gb": 0.0,
            "max_per_host_resource_reservation_mb": 0.0,
            "peak_memory_mb": 0.0,
            "peak_memory_gb": 0.0,
            "spill_detected": False,
            "spill_count": 0,
            "scratch_bytes_written": 0
        }

        # --------------------------------------------------
        # Cluster Memory Admitted
        # --------------------------------------------------

        admitted = re.search(
            r"Cluster Memory Admitted:\s*([\d.]+)\s*GB",
            text,
            re.IGNORECASE
        )

        if admitted:
            result["cluster_memory_admitted_gb"] = float(
                admitted.group(1)
            )

        # --------------------------------------------------
        # Per Host Memory Estimate
        # --------------------------------------------------

        estimate_patterns = [

            r"Per[- ]Host Memory Estimate[: ]+([\d.]+)\s*GB",

            r"Estimated Per[- ]Host Mem(?:ory)?[: ]+([\d.]+)\s*GB",

            r"mem-estimate=([\d.]+)\s*GB",

            r"Memory Estimate[: ]+([\d.]+)\s*GB"
        ]

        for pattern in estimate_patterns:

            m = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if m:
                result["per_host_memory_estimate_gb"] = float(
                    m.group(1)
                )
                break

        # --------------------------------------------------
        # Resource Reservation
        # --------------------------------------------------

        reservation_patterns = [

            r"Max Per[- ]Host Resource Reservation[: ]+([\d.]+)\s*MB",

            r"Per[- ]Host Resource Reservation[: ]+([\d.]+)\s*MB",

            r"Resource Reservation[: ]+([\d.]+)\s*MB"
        ]

        for pattern in reservation_patterns:

            m = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if m:
                result[
                    "max_per_host_resource_reservation_mb"
                ] = float(
                    m.group(1)
                )
                break

        # --------------------------------------------------
        # Peak Memory Extraction
        # --------------------------------------------------

        peak_patterns = [

            r"Peak Memory Usage[: ]+([\d.]+)\s*(MB|GB)",

            r"Peak Mem(?:ory)?(?: Consumption)?[: ]+([\d.]+)\s*(MB|GB)",

            r"Memory Usage[: ]+([\d.]+)\s*(MB|GB)",

            r"PeakMem[: ]+([\d.]+)\s*(MB|GB)"
        ]

        max_peak_mb = 0.0

        for pattern in peak_patterns:

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            for value, unit in matches:

                value = float(value)

                if unit.upper() == "GB":
                    value *= 1024

                max_peak_mb = max(
                    max_peak_mb,
                    value
                )

        result["peak_memory_mb"] = round(
            max_peak_mb,
            2
        )

        result["peak_memory_gb"] = round(
            max_peak_mb / 1024,
            2
        )

        # --------------------------------------------------
        # Spill Detection
        # --------------------------------------------------

        scratch_writes = re.findall(
            r"ScratchWrites[: ]+([0-9,]+)",
            text,
            re.IGNORECASE
        )

        scratch_bytes = re.findall(
            r"ScratchBytesWritten[: ]+([0-9,]+)",
            text,
            re.IGNORECASE
        )

        spill_count = sum(
            int(x.replace(",", ""))
            for x in scratch_writes
        )

        scratch_bytes_written = sum(
            int(x.replace(",", ""))
            for x in scratch_bytes
        )

        spill_detected = (
            spill_count > 0
            or scratch_bytes_written > 0
        )

        result["spill_detected"] = spill_detected
        result["spill_count"] = spill_count
        result["scratch_bytes_written"] = (
            scratch_bytes_written
        )

        # --------------------------------------------------
        # Memory Health
        # --------------------------------------------------

        estimate = result[
            "per_host_memory_estimate_gb"
        ]

        peak_gb = result[
            "peak_memory_gb"
        ]

        if estimate > 0:

            utilization_pct = (
                peak_gb / estimate
            ) * 100

            result[
                "memory_utilization_pct"
            ] = round(
                utilization_pct,
                1
            )

            if utilization_pct < 50:
                result["memory_health"] = "GOOD"

            elif utilization_pct < 80:
                result["memory_health"] = "WARNING"

            else:
                result["memory_health"] = "CRITICAL"

        else:

            result[
                "memory_utilization_pct"
            ] = 0

            result["memory_health"] = "UNKNOWN"

        return result

