"""Data transformation helpers for Oura API responses.

Converts raw API data into more human-readable formats:
- Durations from seconds to "Xh Ym" strings
- ISO timestamps to readable times
- Strips internal IDs that add noise for LLM consumers
"""

from datetime import datetime


def format_duration(seconds: int | float | None) -> str | None:
    """Convert seconds to a human-readable duration string.

    Examples: 27000 -> "7h 30m", 90 -> "1m 30s", 3600 -> "1h 0m"
    """
    if seconds is None:
        return None
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    if minutes > 0:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


def format_timestamp(iso_str: str | None) -> str | None:
    """Convert an ISO 8601 timestamp to a readable time string.

    Returns time-only (e.g. "10:30 PM") for sleep-related times,
    or full datetime if parsing fails partially.
    """
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%-I:%M %p, %b %-d")
    except (ValueError, TypeError):
        return iso_str


def strip_ids(record: dict) -> dict:
    """Remove internal Oura 'id' field from a record."""
    return {k: v for k, v in record.items() if k != "id"}


# -- Per-domain transforms --
# Each takes a list of raw API records and returns a transformed list.


def transform_sleep_sessions(data: list[dict]) -> list[dict]:
    """Transform detailed sleep session data with readable durations and times."""
    duration_fields = [
        "total_sleep_duration",
        "awake_time",
        "light_sleep_duration",
        "deep_sleep_duration",
        "rem_sleep_duration",
        "sleep_phase_5_min",  # skip this one, it's a raw string
        "time_in_bed",
        "latency",
    ]
    time_fields = ["bedtime_start", "bedtime_end"]

    results = []
    for record in data:
        r = strip_ids(record)
        for field in duration_fields:
            if field in r and isinstance(r[field], (int, float)):
                r[field] = format_duration(r[field])
        for field in time_fields:
            if field in r:
                r[field] = format_timestamp(r[field])
        results.append(r)
    return results


def transform_daily_activity(data: list[dict]) -> list[dict]:
    """Transform daily activity with readable time durations."""
    duration_fields = [
        "sedentary_time",
        "resting_time",
        "low_activity_time",
        "medium_activity_time",
        "high_activity_time",
        "non_wear_time",
    ]

    results = []
    for record in data:
        r = strip_ids(record)
        for field in duration_fields:
            if field in r and isinstance(r[field], (int, float)):
                r[field] = format_duration(r[field])
        results.append(r)
    return results


def transform_workouts(data: list[dict]) -> list[dict]:
    """Transform workout data with readable durations and timestamps."""
    results = []
    for record in data:
        r = strip_ids(record)
        if "duration" in r and isinstance(r["duration"], (int, float)):
            r["duration"] = format_duration(r["duration"])
        for field in ("start_datetime", "end_datetime"):
            if field in r:
                r[field] = format_timestamp(r[field])
        results.append(r)
    return results


def transform_sessions(data: list[dict]) -> list[dict]:
    """Transform session data with readable durations and timestamps."""
    # Same shape as workouts
    return transform_workouts(data)


def transform_heart_rate(data: list[dict]) -> list[dict]:
    """Transform heart rate time series with readable timestamps."""
    results = []
    for record in data:
        r = dict(record)
        if "timestamp" in r:
            r["timestamp"] = format_timestamp(r["timestamp"])
        results.append(r)
    return results


def transform_sleep_time(data: list[dict]) -> list[dict]:
    """Transform sleep time recommendations with readable timestamps."""
    time_fields = [
        "optimal_bedtime_start",
        "optimal_bedtime_end",
        "recommendation_start",
        "recommendation_end",
    ]
    results = []
    for record in data:
        r = strip_ids(record)
        # These fields may be nested under an "optimal_bedtime" object
        for field in time_fields:
            if field in r:
                r[field] = format_timestamp(r[field])
        # Handle nested optimal_bedtime object
        if "optimal_bedtime" in r and isinstance(r["optimal_bedtime"], dict):
            ob = r["optimal_bedtime"]
            for key in ("day_tz", "start_offset", "end_offset"):
                pass  # keep numeric offsets as-is
        results.append(r)
    return results


def transform_simple(data: list[dict]) -> list[dict]:
    """Strip IDs from records that need no other transformation.

    Used for: daily_sleep, daily_readiness, daily_resilience, daily_stress,
    daily_spo2, daily_cardiovascular_age, tags, enhanced_tags,
    ring_configuration, rest_mode_period, vo2_max.
    """
    return [strip_ids(record) for record in data]
