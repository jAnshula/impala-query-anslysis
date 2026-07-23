import re

from models.fragment_instance import (
    FragmentInstance
)


class FragmentInstanceExtractor:

    def parse(self, text, query_id=""):

        results = []

        current_fragment = ""

        lines = text.splitlines()

        #
        # PASS 1
        # Build instance list
        #
        for line in lines:

            #
            # Fragment detection
            #
            fm = re.search(
                r"(F\d+):PLAN FRAGMENT",
                line,
                re.I
            )

            if fm:
                current_fragment = fm.group(1)

            else:

                fm = re.search(
                    r"PLAN FRAGMENT\s+(F?\d+)",
                    line,
                    re.I
                )

                if fm:

                    fragment_id = fm.group(1)

                    if not fragment_id.startswith("F"):
                        fragment_id = (
                            "F"
                            + fragment_id
                        )

                    current_fragment = fragment_id

            #
            # Instance
            #
            inst = re.search(
                r"Instance\s+([A-Za-z0-9:_-]+)",
                line,
                re.I
            )

            host = re.search(
                r"host=([^\s\)]+)",
                line,
                re.I
            )

            if inst and host:

                obj = FragmentInstance()

                obj.query_id = query_id

                obj.fragment = current_fragment

                obj.instance_id = (
                    inst.group(1)
                )

                obj.host = (
                    host.group(1)
                )

                results.append(obj)

        #
        # Build lookup map
        #
        instance_map = {
            x.instance_id: x
            for x in results
        }

        #
        # PASS 2
        # Attach metrics
        #
        current = None

        for line in lines:

            start = re.search(
                r"Instance\s+([A-Za-z0-9:_-]+)",
                line,
                re.I
            )

            if start:

                instance_id = (
                    start.group(1)
                )

                current = (
                    instance_map.get(
                        instance_id
                    )
                )

                continue

            if current is None:
                continue

            #
            # Runtime
            #
            runtime = re.search(
                r"CompletionTime:\s*([\d\.]+)(ms|s)",
                line,
                re.I
            )

            if runtime:

                value = float(
                    runtime.group(1)
                )

                unit = runtime.group(2)

                if unit.lower() == "s":
                    value *= 1000

                current.runtime_ms = int(
                    value
                )

            #
            # Rows
            #
            rows = re.search(
                r"(RowsProduced|RowsReturned|RowsRead):\s*([\d,]+)",
                line,
                re.I
            )

            if rows:

                current.rows = int(
                    rows.group(2)
                    .replace(",", "")
                )

            #
            # Peak Memory
            #
            mem = re.search(
                r"Peak.*?:\s*([\d\.]+)\s*(KB|MB|GB)",
                line,
                re.I
            )

            if mem:

                value = float(
                    mem.group(1)
                )

                unit = mem.group(2).upper()

                if unit == "GB":
                    value *= (
                        1024
                        * 1024
                        * 1024
                    )

                elif unit == "MB":
                    value *= (
                        1024
                        * 1024
                    )

                elif unit == "KB":
                    value *= 1024

                current.peak_memory = int(
                    value
                )

            #
            # IO Wait
            #
            io = re.search(
                r"ScannerIoWaitTime:\s*([\d\.]+)",
                line,
                re.I
            )

            if io:

                current.io_wait_ms = int(
                    float(
                        io.group(1)
                    )
                )

            #
            # Network Receive
            #
            net_recv = re.search(
                r"TotalNetworkReceiveTime:\s*([\d\.]+)",
                line,
                re.I
            )

            if net_recv:

                current.network_receive_ms = int(
                    float(
                        net_recv.group(1)
                    )
                )

            #
            # Network Send
            #
            net_send = re.search(
                r"TotalNetworkSendTime:\s*([\d\.]+)",
                line,
                re.I
            )

            if net_send:

                current.network_send_ms = int(
                    float(
                        net_send.group(1)
                    )
                )

            #
            # Bytes Read
            #
            read_match = re.search(
                r"BytesRead:\s*([\d,]+)",
                line,
                re.I
            )

            if read_match:

                current.read_bytes = int(
                    read_match.group(1)
                    .replace(",", "")
                )

            #
            # Bytes Written
            #
            write_match = re.search(
                r"BytesWritten:\s*([\d,]+)",
                line,
                re.I
            )

            if write_match:

                current.write_bytes = int(
                    write_match.group(1)
                    .replace(",", "")
                )

            #
            # Spill Bytes
            #
            spill_match = re.search(
                r"SpilledBytes:\s*([\d,]+)",
                line,
                re.I
            )
            if spill_match:
                current.spill_bytes = int(
                    spill_match.group(1).replace(",", "")
                )

            #
            # Bytes Sent
            #
            sent_match = re.search(
                r"BytesSent:\s*([\d,]+)",
                line,
                re.I
            )
            if sent_match:
                current.bytes_sent = int(
                    sent_match.group(1).replace(",", "")
                )

            #
            # Scanner Time
            #
            scanner_time = re.search(
                r"ScannerTime:\s*([\d\.]+)(ms|s)?",
                line,
                re.I
            )
            if scanner_time:
                value = float(scanner_time.group(1))
                unit = scanner_time.group(2) or "ms"
                if unit.lower() == "s":
                    value *= 1000
                current.scanner_time_ms = int(value)

            #
            # Scanner Threads
            #
            scanner_threads = re.search(
                r"ScannerThreads:\s*([\d,]+)",
                line,
                re.I
            )
            if scanner_threads:
                current.scanner_threads = int(
                    scanner_threads.group(1).replace(",", "")
                )


            return results

