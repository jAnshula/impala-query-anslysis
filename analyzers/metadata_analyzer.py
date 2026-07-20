import re

class MetadataAnalyzer:

    def analyze(self, profile):

        findings = []

        text = getattr(
            profile,
            "raw_profile",
            ""
        )

        if (
            "PARTITION_NOT_FOUND"
            in text
        ):

            findings.append(
                {
                    "category":
                        "metadata",

                    "severity":
                        "critical",

                    "title":
                        "Partition Metadata Failure",

                    "description":
                        (
                            "PARTITION_NOT_FOUND "
                            "encountered during planning."
                        )
                }
            )

        return findings

