import re


class NetworkExtractor:
    """
    Extract network metrics from Impala profile.

    Examples:

    TotalBytesSent: 14.1 MB
    TotalBytesReceived: 14.1 MB

    RpcWriteTime: 3.02s
    RpcReadTime: 144ms
    """

    def parse(self, text: str):

        result = {
            "bytes_sent": 0.0,
            "bytes_received": 0.0,
            "rpc_write_time": 0.0,
            "rpc_read_time": 0.0
        }

        sent_match = re.search(
            r"TotalBytesSent.*?([\d\.]+)\s*MB",
            text,
            re.IGNORECASE
        )

        if sent_match:
            result["bytes_sent"] = float(
                sent_match.group(1)
            )

        recv_match = re.search(
            r"TotalBytesReceived.*?([\d\.]+)\s*MB",
            text,
            re.IGNORECASE
        )

        if recv_match:
            result["bytes_received"] = float(
                recv_match.group(1)
            )

        rpc_write_sec = re.search(
            r"RpcWriteTime.*?([\d\.]+)s",
            text,
            re.IGNORECASE
        )

        if rpc_write_sec:
            result["rpc_write_time"] = float(
                rpc_write_sec.group(1)
            )

        rpc_read_ms = re.search(
            r"RpcReadTime.*?([\d\.]+)ms",
            text,
            re.IGNORECASE
        )

        if rpc_read_ms:
            result["rpc_read_time"] = (
                float(
                    rpc_read_ms.group(1)
                )
                / 1000
            )

        return result

