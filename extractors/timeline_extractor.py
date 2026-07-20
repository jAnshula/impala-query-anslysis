import re

from models.timeline import Timeline


class TimelineExtractor:

    DURATION_PATTERN = re.compile(
        r'(?P<event>.+?)\s*:\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>ms|s|m|min|minutes|h)',
        re.IGNORECASE
    )

    TIMESTAMP_PATTERN = re.compile(
        r'^(.*?)\s*:\s*.*?\((\d+)\)\s*$',
        re.IGNORECASE
    )

    QUERY_TIMELINE_PATTERN = re.compile(
        r'''
        Planning\ finished:\s*
        (?P<planning>[0-9.]+)m.*?

        Completed\ admission:\s*
        (?P<admission>[0-9.]+)m.*?

        Last\ row\ fetched:\s*
        (?P<execution>[0-9.]+)m
        ''',
        re.S | re.X | re.I
    )

    def parse_duration(
        self,
        value,
        unit
    ):

        value = float(value)

        unit = unit.lower()

        if unit == "ms":
            return int(value)

        if unit == "s":
            return int(value * 1000)

        if unit in [
            "m",
            "min",
            "minutes"
        ]:
            return int(
                value * 60 * 1000
            )

        if unit == "h":
            return int(
                value * 60 * 60 * 1000
            )

        return 0

    def parse(
        self,
        text
    ):

        events = {}
        timestamps = {}

        #
        # PASS 1
        # Query Timeline Section
        #
        timeline_match = (
            self.QUERY_TIMELINE_PATTERN
            .search(text)
        )

        if timeline_match:

            planning_min = float(
                timeline_match.group(
                    "planning"
                )
            )

            admission_end_min = float(
                timeline_match.group(
                    "admission"
                )
            )

            execution_end_min = float(
                timeline_match.group(
                    "execution"
                )
            )

            planning_ms = int(
                planning_min
                * 60
                * 1000
            )

            admission_ms = int(
                (
                    admission_end_min
                    - planning_min
                )
                * 60
                * 1000
            )

            execution_ms = int(
                (
                    execution_end_min
                    - admission_end_min
                )
                * 60
                * 1000
            )

            total_ms = int(
                execution_end_min
                * 60
                * 1000
            )

            events.update(
                {
                    "planning_ms":
                        planning_ms,
                    "admission_ms":
                        admission_ms,
                    "execution_ms":
                        execution_ms,
                    "total_ms":
                        total_ms
                }
            )

        #
        # PASS 2
        # Generic parsing
        #
        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            ts_match = (
                self.TIMESTAMP_PATTERN
                .search(line)
            )

            if ts_match:

                event = (
                    ts_match.group(1)
                    .strip()
                )

                timestamp_ns = int(
                    ts_match.group(2)
                )

                timestamps[
                    event
                ] = timestamp_ns

            duration_match = (
                self.DURATION_PATTERN
                .search(line)
            )

            if duration_match:

                event = (
                    duration_match
                    .group("event")
                    .strip()
                )

                duration = (
                    self.parse_duration(
                        duration_match.group(
                            "value"
                        ),
                        duration_match.group(
                            "unit"
                        )
                    )
                )

                if event not in events:

                    events[event] = duration

        #
        # PASS 3
        # Timestamp derivation
        #
        if timestamps:

            if (
                "planning_ms"
                not in events
                and
                "Planning finished"
                in timestamps
            ):

                events[
                    "planning_ms"
                ] = int(
                    timestamps[
                        "Planning finished"
                    ]
                    /
                    1_000_000
                )

            if (
                "admission_ms"
                not in events
                and
                "Completed admission"
                in timestamps
                and
                "Planning finished"
                in timestamps
            ):

                events[
                    "admission_ms"
                ] = int(
                    (
                        timestamps[
                            "Completed admission"
                        ]
                        -
                        timestamps[
                            "Planning finished"
                        ]
                    )
                    /
                    1_000_000
                )

            execution_start = None

            for key in timestamps:

                if key.startswith(
                    "Ready to start on"
                ):
                    execution_start = (
                        timestamps[key]
                    )
                    break

            if (
                "execution_ms"
                not in events
            ):

                if (
                    execution_start
                    and
                    "Last row fetched"
                    in timestamps
                ):

                    events[
                        "execution_ms"
                    ] = int(
                        (
                            timestamps[
                                "Last row fetched"
                            ]
                            -
                            execution_start
                        )
                        /
                        1_000_000
                    )

                elif (
                    "Completed admission"
                    in timestamps
                    and
                    "Last row fetched"
                    in timestamps
                ):

                    events[
                        "execution_ms"
                    ] = int(
                        (
                            timestamps[
                                "Last row fetched"
                            ]
                            -
                            timestamps[
                                "Completed admission"
                            ]
                        )
                        /
                        1_000_000
                    )

        #
        # PASS 4
        # Retry extraction
        #
        retry_match = re.search(
            r"Retried query planning due to inconsistent metadata\s+(\d+)\s+of\s+(\d+)",
            text,
            re.IGNORECASE
        )

        if retry_match:

            events[
                "planning_retry_count"
            ] = int(
                retry_match.group(1)
            )

            events[
                "planning_retry_limit"
            ] = int(
                retry_match.group(2)
            )

        #
        # PASS 5
        # Safety validation
        #
        planning = events.get(
            "planning_ms",
            0
        )

        admission = events.get(
            "admission_ms",
            0
        )

        execution = events.get(
            "execution_ms",
            0
        )

        total = events.get(
            "total_ms",
            0
        )

        if (
            total == 0
            and
            (
                planning
                or admission
                or execution
            )
        ):

            events[
                "total_ms"
            ] = (
                planning
                + admission
                + execution
            )

        return Timeline(
            events=events
        )


