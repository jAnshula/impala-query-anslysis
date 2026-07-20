import re

from models.exec_summary import (
    ExecSummary,
    ExecSummaryFragment,
    ExecSummaryOperator
)


class ExecSummaryExtractor:

    def _normalize_fragment_id(
        self,
        fragment_id
    ):

        fragment_id = str(
            fragment_id
        ).strip()

        if not fragment_id.upper().startswith("F"):

            fragment_id = (
                "F"
                + fragment_id
            )

        return fragment_id.upper()

    def parse(self, text):

        fragments = []

        current_fragment = None

        for line in text.splitlines():

            line = line.rstrip()

            #
            # Fragment Header
            #
            fragment_match = re.search(
                r"Fragment\s+(F?\d+)",
                line,
                re.I
            )

            if fragment_match:

                if current_fragment:
                    fragments.append(
                        current_fragment
                    )

                current_fragment = (
                    ExecSummaryFragment(
                        fragment_id=
                            self._normalize_fragment_id(
                                fragment_match.group(1)
                            ),
                        operators=[],
                        host_count=0,
                        instance_count=0
                    )
                )

                continue

            if current_fragment is None:
                continue

            #
            # Hosts
            #
            host_match = re.search(
                r"Hosts?:\s*(\d+)",
                line,
                re.I
            )

            if host_match:

                current_fragment.host_count = int(
                    host_match.group(1)
                )

            #
            # Instances
            #
            instance_match = re.search(
                r"Instances?:\s*(\d+)",
                line,
                re.I
            )

            if instance_match:

                current_fragment.instance_count = int(
                    instance_match.group(1)
                )

            #
            # Operator rows
            #
            table_row = re.match(
                r'^\s*(\d+):([A-Z_ ]+)',
                line
            )

            if not table_row:
                continue

            operator_id = int(
                table_row.group(1)
            )

            operator_type = (
                table_row.group(2)
                .strip()
            )

            #
            # Parse optional metrics
            #
            avg_time_ms = 0
            max_time_ms = 0
            rows_produced = 0
            peak_memory_bytes = 0
            est_peak_memory_bytes = 0

            avg_match = re.search(
                r"avg.*?([\d,]+)\s*ms",
                line,
                re.I
            )

            if avg_match:

                avg_time_ms = int(
                    avg_match.group(1)
                    .replace(",", "")
                )

            max_match = re.search(
                r"max.*?([\d,]+)\s*ms",
                line,
                re.I
            )

            if max_match:

                max_time_ms = int(
                    max_match.group(1)
                    .replace(",", "")
                )

            rows_match = re.search(
                r"([\d,]+)\s*rows",
                line,
                re.I
            )

            if rows_match:

                rows_produced = int(
                    rows_match.group(1)
                    .replace(",", "")
                )

            operator = ExecSummaryOperator(

                operator_id=operator_id,

                operator_type=operator_type,

                fragment_id=
                    current_fragment.fragment_id,

                avg_time_ms=
                    avg_time_ms,

                max_time_ms=
                    max_time_ms,

                rows_produced=
                    rows_produced,

                peak_memory_bytes=
                    peak_memory_bytes,

                est_peak_memory_bytes=
                    est_peak_memory_bytes
            )

            current_fragment.operators.append(
                operator
            )

        if current_fragment:

            fragments.append(
                current_fragment
            )

        return ExecSummary(
            fragments=fragments
        )

