def ms_to_hms(ms):
    """Convert milliseconds to HH:MM:SS.mmm format."""
    try:
        total_ms = int(ms)
    except Exception:
        return str(ms)

    if total_ms < 0:
        total_ms = 0

    total_seconds, millis = divmod(total_ms, 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"

