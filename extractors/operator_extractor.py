import re

class OperatorExtractor:
    def parse(self, text: str):
        operators = []
        current_fragment = None
        lines = text.splitlines()

        fragment_pattern = re.compile(r"Fragment\s+(F\d+)")
        operator_pattern = re.compile(r"(\d+):([A-Z_ ]+)")
        runtime_pattern_minsec = re.compile(r"(\d+)m(\d+)s")
        runtime_pattern_sec = re.compile(r"(\d+)s")
        runtime_pattern_ms = re.compile(r"(\d+)ms")
        memory_pattern = re.compile(r"([\d\.]+)\s+GB")

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Fragment
            fragment_match = fragment_pattern.search(line)
            if fragment_match:
                current_fragment = fragment_match.group(1)

            # Operator
            operator_match = operator_pattern.search(line)
            if operator_match:
                node = operator_match.group(1)
                operator = operator_match.group(2).replace("_", " ").title()

                runtime_seconds = 0
                peak_memory_gb = 0

                # Look ahead for runtime/memory
                lookahead = lines[i:min(i + 15, len(lines))]
                for entry in lookahead:
                    # Match XmYs
                    m = runtime_pattern_minsec.search(entry)
                    if m:
                        mins = int(m.group(1))
                        secs = int(m.group(2))
                        runtime_seconds = mins * 60 + secs
                        continue

                    # Match Xs
                    m = runtime_pattern_sec.search(entry)
                    if m:
                        runtime_seconds = int(m.group(1))
                        continue

                    # Match Xms
                    m = runtime_pattern_ms.search(entry)
                    if m:
                        runtime_seconds = int(m.group(1)) / 1000.0
                        continue

                    # Memory
                    mem = memory_pattern.search(entry)
                    if mem:
                        peak_memory_gb = float(mem.group(1))

                operators.append({
                    "fragment": current_fragment,
                    "node": node,
                    "operator": operator,
                    "runtime_seconds": runtime_seconds,
                    "peak_memory_gb": peak_memory_gb
                })

            i += 1

        return operators

