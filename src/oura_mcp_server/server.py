"""MCP server exposing Oura Ring API v2 data as tools."""

import json
import os

from mcp.server.fastmcp import FastMCP

from oura_mcp_server.client import OuraClient
from oura_mcp_server.transforms import (
    transform_daily_activity,
    transform_heart_rate,
    transform_sessions,
    transform_simple,
    transform_sleep_sessions,
    transform_sleep_time,
    transform_workouts,
)

mcp = FastMCP("Oura Ring")


def _get_client() -> OuraClient:
    """Create an OuraClient from the OURA_API_TOKEN env var."""
    token = os.environ.get("OURA_API_TOKEN")
    if not token:
        raise ValueError(
            "OURA_API_TOKEN environment variable is required. "
            "Get a Personal Access Token from https://cloud.ouraring.com/personal-access-tokens"
        )
    return OuraClient(token)


def _to_json(data: object) -> str:
    """Serialize data to indented JSON string for LLM consumption."""
    return json.dumps(data, indent=2, default=str)


# -- Sleep & Recovery --


@mcp.tool()
async def get_sleep_data(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get detailed sleep session data including sleep stages, heart rate, HRV, and breathing rate.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_sleep(start_date, end_date)
    return _to_json(transform_sleep_sessions(data))


@mcp.tool()
async def get_daily_sleep(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get daily sleep scores and contributor breakdown (deep sleep, efficiency, latency, REM, restfulness, timing).

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_daily_sleep(start_date, end_date)
    return _to_json(transform_simple(data))


@mcp.tool()
async def get_sleep_time(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get recommended and actual sleep timing windows.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_sleep_time(start_date, end_date)
    return _to_json(transform_sleep_time(data))


@mcp.tool()
async def get_daily_readiness(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get readiness scores and contributors (activity balance, body temperature, HRV balance, resting heart rate, sleep balance).

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_daily_readiness(start_date, end_date)
    return _to_json(transform_simple(data))


@mcp.tool()
async def get_daily_resilience(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get resilience data indicating recovery capacity and stress tolerance.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_daily_resilience(start_date, end_date)
    return _to_json(transform_simple(data))


# -- Activity & Fitness --


@mcp.tool()
async def get_daily_activity(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get daily activity data including steps, calories, active time breakdown, and MET levels.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_daily_activity(start_date, end_date)
    return _to_json(transform_daily_activity(data))


@mcp.tool()
async def get_workouts(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get workout sessions with activity type, calories burned, distance, intensity, and duration.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_workouts(start_date, end_date)
    return _to_json(transform_workouts(data))


@mcp.tool()
async def get_sessions(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get guided and unguided session data (meditation, breathing, etc.) with heart rate and HRV biometrics.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_sessions(start_date, end_date)
    return _to_json(transform_sessions(data))


@mcp.tool()
async def get_vo2_max(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get VO2 max estimates indicating cardiovascular fitness level.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_vo2_max(start_date, end_date)
    return _to_json(transform_simple(data))


# -- Health Vitals --


@mcp.tool()
async def get_heart_rate(
    start_datetime: str | None = None, end_datetime: str | None = None
) -> str:
    """Get heart rate data at 5-minute intervals throughout the day and night.

    Args:
        start_datetime: Start datetime in YYYY-MM-DDTHH:MM:SS format. Defaults to ~24 hours ago.
        end_datetime: End datetime in YYYY-MM-DDTHH:MM:SS format. Defaults to now.
    """
    async with _get_client() as client:
        data = await client.get_heart_rate(start_datetime, end_datetime)
    return _to_json(transform_heart_rate(data))


@mcp.tool()
async def get_daily_spo2(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get daily blood oxygen (SpO2) saturation readings.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_daily_spo2(start_date, end_date)
    return _to_json(transform_simple(data))


@mcp.tool()
async def get_daily_stress(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get daily stress levels including stress high, recovery high, and day summary.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_daily_stress(start_date, end_date)
    return _to_json(transform_simple(data))


@mcp.tool()
async def get_daily_cardiovascular_age(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get estimated cardiovascular age based on resting heart rate and HRV trends.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_daily_cardiovascular_age(start_date, end_date)
    return _to_json(transform_simple(data))


# -- User & Device --


@mcp.tool()
async def get_personal_info() -> str:
    """Get user profile information including age, weight, height, and biological sex."""
    async with _get_client() as client:
        data = await client.get_personal_info()
    return _to_json(data)


@mcp.tool()
async def get_ring_configuration(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get ring hardware details including model, color, firmware version, and setup date.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_ring_configuration(start_date, end_date)
    return _to_json(transform_simple(data))


@mcp.tool()
async def get_rest_mode(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get rest mode periods and their scheduled episodes.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        data = await client.get_rest_mode_period(start_date, end_date)
    return _to_json(transform_simple(data))


# -- Tags --


@mcp.tool()
async def get_tags(
    start_date: str | None = None, end_date: str | None = None
) -> str:
    """Get user-created tags and lifestyle annotations (e.g. caffeine, alcohol, exercise notes).

    Returns enhanced tags when available, falling back to standard tags.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to yesterday.
        end_date: End date in YYYY-MM-DD format. Defaults to today.
    """
    async with _get_client() as client:
        # Try enhanced tags first, fall back to standard tags
        data = await client.get_enhanced_tags(start_date, end_date)
        if not data:
            data = await client.get_tags(start_date, end_date)
    return _to_json(transform_simple(data))


def main() -> None:
    """Entry point for the oura-mcp-server command."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
