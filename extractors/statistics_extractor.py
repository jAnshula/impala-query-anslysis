# extractors/statistics_extractor.py
import re

class StatisticsExtractor:
    def extract(self, profile):
        raw = getattr(profile, "raw_profile", "")
        return self.parse(raw)

    def parse(self, text: str):
        result = {
            "missing_stats": False,
            "corrupt_stats": False,
            "stats_warnings": [],
            "tables_with_missing_stats": [],
        }

        # Detect missing statistics
        if re.search(r"missing relevant table and/or column statistics", text, re.I):
            result["missing_stats"] = True
            result["stats_warnings"].append("Missing relevant table/column statistics")

        # Detect corrupt statistics
        if re.search(r"corrupt statistics", text, re.I):
            result["corrupt_stats"] = True
            result["stats_warnings"].append("Corrupt statistics detected")

        # Optional: capture table names with missing stats
        table_matches = re.findall(r"Table: (\S+).*missing statistics", text, re.I)
        if table_matches:
            result["tables_with_missing_stats"] = table_matches

        return result


