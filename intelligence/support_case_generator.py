class SupportCaseGenerator:

    def generate(
        self,
        root_causes
    ):

        output = []

        output.append(
            "Root Cause Analysis"
        )

        output.append(
            "=" * 60
        )

        for cause in root_causes:

            output.append(
                f"Cause: {cause.title}"
            )

            output.append(
                f"Severity: {cause.severity}"
            )

            output.append(
                f"Confidence: "
                f"{cause.confidence}"
            )

            output.append("Evidence:")

            for evidence in cause.evidence:

                output.append(
                    f"  - {evidence}"
                )

        return "\n".join(output)


