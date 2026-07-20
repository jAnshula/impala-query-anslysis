from analyzers.findings import Finding

class RootCauseChainBuilder:
    def build(self, profile, analytics, intelligence):
        chain = []

        scan = profile.scan_metrics or {}
        memory = profile.memory_metrics or {}

        rows_read = scan.get("rows_read", 0)
        if rows_read > 0:
            if rows_read >= 1_000_000:
                chain.append(f"SCAN {rows_read/1_000_000:.1f}M rows")
            else:
                chain.append(f"SCAN {rows_read:,} rows")

        findings = analytics.get("findings", [])

        titles = []
        for x in findings:
            if isinstance(x, dict):
                titles.append(x.get("title", "").lower())
            elif isinstance(x, Finding):
                titles.append(x.title.lower())
            else:
                titles.append(str(x).lower())

        if any("nested loop" in t for t in titles):
            chain.append("Nested Loop Join")

        if any("fragment runtime skew" in t for t in titles):
            chain.append("Execution Skew")

        peak_memory = memory.get("peak_memory_gb", 0)
        if peak_memory > 0:
            chain.append(f"{peak_memory:.1f} GB Memory")

        runtime_ms = profile.timeline.get("Execution", 0)
        if runtime_ms:
            runtime_min = (runtime_ms / 1000) / 60
            chain.append(f"{runtime_min:.1f} Minute Runtime")

        result_rows = scan.get("rows_returned", 0)
        if result_rows:
            chain.append(f"{result_rows:,} Rows Returned")

        return chain

