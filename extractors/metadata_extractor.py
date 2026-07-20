import re

class MetadataExtractor:
    def extract(self, profile):
        raw = getattr(profile, "raw_profile", "")
        return self.parse(raw)

    def parse(self, text):
        result = {}

        result["partition_not_found"] = len(
            re.findall(r"PARTITION_NOT_FOUND", text, re.I)
        )

        retry_match = re.search(
            r"Retried query planning due to inconsistent metadata\s+(\d+)\s+of\s+(\d+)",
            text,
            re.I
        )
        if retry_match:
            result["planning_retries"] = int(retry_match.group(1))
            result["retry_attempts"] = int(retry_match.group(2))
            result["inconsistent_metadata"] = True
        else:
            result["planning_retries"] = len(
                re.findall(r"Retried query planning", text, re.I)
            )
            result["retry_attempts"] = 0
            result["inconsistent_metadata"] = False

        result["catalog_fetches"] = len(re.findall(r"CatalogFetch", text, re.I))
        result["metadata_loads"] = len(re.findall(r"LoadTableMetadata", text, re.I))
        result["authorization_checks"] = len(re.findall(r"Authorization", text, re.I))

        result["compute_stats_missing"] = (
            "missing relevant table and/or column statistics" in text.lower()
        )
        result["missing_stats"] = (
            "missing relevant table and/or column statistics" in text.lower()
        )
        result["corrupt_statistics"] = "corrupt statistics" in text.lower()

        return result

