import re


class ResourceExtractor:

    def parse(self, text):

        result = {

            "cpu_ms": 0,

            "peak_memory": 0

        }

        #
        # TotalCpuTime
        #

        m = re.search(
            r"TotalCpuTime:\s*(.*)",
            text
        )

        if m:

            raw = m.group(1)

            total_ms = 0

            h = re.search(
                r"(\d+)h",
                raw
            )

            mins = re.search(
                r"(\d+)m",
                raw
            )

            secs = re.search(
                r"(\d+)s",
                raw
            )

            if h:
                total_ms += (
                    int(h.group(1))
                    * 3600000
                )

            if mins:
                total_ms += (
                    int(mins.group(1))
                    * 60000
                )

            if secs:
                total_ms += (
                    int(secs.group(1))
                    * 1000
                )

            result["cpu_ms"] = total_ms

        return result

