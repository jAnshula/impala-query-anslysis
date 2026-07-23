from dataclasses import dataclass


@dataclass
class QueryInfo:
    """Core Impala query metadata and identification.
    
    Represents immutable query information extracted from execution profile.
    """

    query_id: str = ""
    """Unique Impala query identifier"""

    session_id: str = ""
    """Unique Impala query session identifier"""

    user: str = ""
    """User who submitted the query"""

    coordinator: str = ""
    """Coordinator node hostname"""

    state: str = ""
    """Final query state (FINISHED, EXCEPTION, etc.)"""

    duration: str = ""
    """Total query execution time (formatted string)"""

    start_time: str = ""
    """Query start timestamp"""

    end_time: str = ""
    """Query end timestamp"""

    pool: str = ""
    """Resource pool name (if applicable)"""

    query_type: str = ""
    """Query type (SELECT, INSERT, etc.)"""