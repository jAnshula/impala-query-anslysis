import re

class ScanExtractor:

    def parse(self, text):
        result = {
            "bytes_read": 0,
            "files_scanned": 0,
            "partitions_scanned": 0,
            "rows_returned": 0,
            "rows_read": 0
        }

        #
        # TotalBytesRead
        #

        m = re.search(
            r"TotalBytesRead.*?([\d\.]+)\s*([TGMK]?B)",
            text,
            re.I
        )

        if m:
            value = float(
                m.group(1)
            )
            unit = (
                m.group(2)
                .upper()
            )
            if unit == "TB":
                value *= 1024**4

            elif unit == "GB":
                value *= 1024**3

            elif unit == "MB":
                value *= 1024**2

            result["bytes_read"] = int(
                value
            )

        #
        # files=
        #

        m = re.search(
            r"files=(\d+)",
            text,
            re.I
        )

        if m:
            result["files_scanned"] = int(
                m.group(1)
            )

        #
        # partitions=
        #

        m = re.search(
            r"partitions=(\d+)",
            text,
            re.I
        )

        if m:
            result["partitions_scanned"] = int(
                m.group(1)
            )

        #
        # RowsReturned
        #

        m = re.search(
            r"RowsReturned:\s*([\d,]+)",
            text,
            re.I
        )

        if m:
            rows_val = int(
                m.group(1)
                .replace(",", "")
            )
            
            result["rows_returned"] = rows_val
            result["rows_read"] = rows_val  # Sync both

        return result