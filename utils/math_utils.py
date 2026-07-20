def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide with zero protection."""
    return numerator / denominator if denominator != 0 else default

def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage safely."""
    return (part / total * 100) if total > 0 else 0.0
