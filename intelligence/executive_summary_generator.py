class ExecutiveSummaryGenerator:
    def generate(self, profile, root_causes, recommendations, findings):
        summary_lines = []

        query_info = getattr(profile, "query_info", None)

        query_id = (
            getattr(query_info, "query_id", None)
            or getattr(profile, "query_id", "UNKNOWN")
        )

        coordinator = (
            getattr(query_info, "coordinator", None)
            or getattr(profile, "coordinator", "UNKNOWN")
        )
        summary_lines.append(f"### Query Information\nQuery ID: {query_id}\nCoordinator: {coordinator}\n")

        # Runtime breakdown
        rb = getattr(profile, "timeline", {})
        if rb:
            summary_lines.append(
                f"### Runtime Breakdown\n"
                f"Planning: {rb.get('planning_label')}\n"
                f"Admission: {rb.get('admission_label')}\n"
                f"Execution: {rb.get('execution_label')}\n"
                f"Total: {rb.get('total_label')}\n"
            )

        # Executive assessment
        if root_causes:

            primary = root_causes[0]

            summary_lines.append("### Executive Assessment")

            summary_lines.append(
                f"Primary root cause identified: "
                f"{primary.title} "
                f"({primary.severity})."
            )

            summary_lines.append("")

            rb = getattr(profile, "runtime_breakdown", {})

            planning_pct = rb.get("planning_pct", 0)

            if planning_pct > 0:
                summary_lines.append(
                    f"Impact: Planning consumed "
                    f"{planning_pct:.1f}% of total runtime."
                )

            summary_lines.append("")

            summary_lines.append(
                "Refer to the Root Cause Analysis "
                "and Recommendations sections for details."
            )

        return "\n".join(summary_lines)

