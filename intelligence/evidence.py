from dataclasses import dataclass


@dataclass
class Evidence:

    source: str

    metric: str

    value: str

