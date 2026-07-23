import re
from models.query_info import QueryInfo

class SummaryExtractor:
    def extract(self, profile):
        raw = getattr(profile, "raw_profile", "")
        return self.parse(raw)

    def parse(self, text):
        def extract(pattern):
            match = re.search(pattern, text, re.MULTILINE)
            return match.group(1).strip() if match else ""

        query_id = extract(r"Query \(id=([^)]+)\)")
        if not query_id:
            query_id = extract(r"Query Id:\s*(.*)")

        user = extract(r"User:\s*(.*)")
        coordinator = extract(r"Coordinator:\s*(.*)")
        state = extract(r"Query State:\s*(.*)")
        start_time = extract(r"Start Time:\s*(.*)")
        end_time = extract(r"End Time:\s*(.*)")
        pool = extract(r"Request Pool:\s*(.*)")

        # Added fields
        duration = extract(r"Duration:\s*(.*)")
        query_type = extract(r"Query Type:\s*(.*)")

        session_id = extract(
            r"Session ID:\s*(.*)"
        )

        return QueryInfo(
            query_id=query_id,
            user=user,
            coordinator=coordinator,
            state=state,
            duration=duration,
            start_time=start_time,
            end_time=end_time,
            pool=pool,
            query_type=query_type,
            session_id=session_id
        )


