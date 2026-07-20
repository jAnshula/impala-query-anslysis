from dataclasses import dataclass

@dataclass
class QueryInfo:
    query_id: str = ""
    user: str = ""
    coordinator: str = ""
    state: str = ""
    duration: str = ""

    start_time: str = ""
    end_time: str = ""

    pool: str = ""
    query_type: str = ""

