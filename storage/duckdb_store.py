import duckdb

class DuckDBStore:

    def __init__(self):

        self.conn = duckdb.connect(
            "impala_intelligence.db"
        )

        self._initialize()

    def _initialize(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS query_profiles (

            query_id TEXT,

            user_name TEXT,

            coordinator TEXT,

            pool TEXT,

            duration_ms BIGINT,

            health_score INTEGER,

            execution_date TIMESTAMP,

            profile_json TEXT
        )
        """)

