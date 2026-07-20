import re


class CPUExtractor:
    """
    Extract CPU usage per host from Impala profile.

    Example lines:

    hostc76 17m15s
    hostc48 684ms
    hostc32 455ms
    """

    def parse(self, text: str):

        cpu_metrics = []

        # host + XmYs
        minute_pattern = re.compile(
            r"([A-Za-z0-9\-_\.]+)\s+(\d+)m(\d+)s"
        )

        # host + Xms
        ms_pattern = re.compile(
            r"([A-Za-z0-9\-_\.]+)\s+(\d+)ms"
        )

        seen_hosts = set()

        for match in minute_pattern.finditer(text):

            host = match.group(1)

            mins = int(match.group(2))
            secs = int(match.group(3))

            total_seconds = mins * 60 + secs

            if host not in seen_hosts:

                cpu_metrics.append(
                    {
                        "host": host,
                        "cpu_seconds": total_seconds
                    }
                )

                seen_hosts.add(host)

        for match in ms_pattern.finditer(text):

            host = match.group(1)

            ms = int(match.group(2))

            total_seconds = round(ms / 1000, 3)

            if host not in seen_hosts:

                cpu_metrics.append(
                    {
                        "host": host,
                        "cpu_seconds": total_seconds
                    }
                )

                seen_hosts.add(host)

        return cpu_metrics

