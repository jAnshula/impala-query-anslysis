from extractors.profile_loader import ProfileLoader
from extractors.timeline_extractor import TimelineExtractor


def test_timeline():

    text=open(
        "sample_profiles/Impala_query_long_running.txt"
    ).read()


    result=TimelineExtractor().parse(text)


    assert result.events["total_ms"] > 0

