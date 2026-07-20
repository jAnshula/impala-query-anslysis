# storage/query_repository.py

import json

class QueryRepository:

    def __init__(self, store):
        self.store = store

    def save_profile(self, profile, analytics):
        self.store.conn.execute(
            """
            INSERT INTO query_profiles
            VALUES (?, ?, ?, ?, ?, ?, NOW(), ?)
            """,
            [
                profile.query_info.query_id,
                profile.query_info.user,
                profile.query_info.coordinator,
                profile.query_info.pool,
                profile.query_info.duration,
                analytics["health_score"],
                json.dumps(profile.__dict__)  # or profile.to_dict() if implemented
            ]
        )

