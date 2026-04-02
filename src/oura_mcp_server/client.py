"""HTTP client for the Oura Ring API v2."""

import httpx


BASE_URL = "https://api.ouraring.com/v2/usercollection"


class OuraClient:
    """Async client for the Oura Ring API v2.

    All public methods return raw JSON dicts/lists from the API.
    Data transformation is handled separately in transforms.py.
    """

    def __init__(self, access_token: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=httpx.Timeout(30.0),
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "OuraClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    async def _get(self, endpoint: str, params: dict[str, str | None] | None = None) -> dict:
        """Make a GET request, return parsed JSON."""
        # Strip None values from params
        cleaned = {k: v for k, v in (params or {}).items() if v is not None}
        resp = await self._client.get(f"/{endpoint}", params=cleaned)
        resp.raise_for_status()
        return resp.json()

    async def _get_collection(
        self, endpoint: str, params: dict[str, str | None] | None = None
    ) -> list[dict]:
        """GET a paginated collection endpoint, following next_token until exhausted."""
        cleaned = {k: v for k, v in (params or {}).items() if v is not None}
        all_data: list[dict] = []

        while True:
            resp = await self._client.get(f"/{endpoint}", params=cleaned)
            resp.raise_for_status()
            body = resp.json()
            all_data.extend(body.get("data", []))

            next_token = body.get("next_token")
            if not next_token:
                break
            cleaned["next_token"] = next_token

        return all_data

    # -- Daily summary endpoints --

    async def get_daily_activity(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "daily_activity", {"start_date": start_date, "end_date": end_date}
        )

    async def get_daily_readiness(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "daily_readiness", {"start_date": start_date, "end_date": end_date}
        )

    async def get_daily_sleep(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "daily_sleep", {"start_date": start_date, "end_date": end_date}
        )

    async def get_daily_spo2(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "daily_spo2", {"start_date": start_date, "end_date": end_date}
        )

    async def get_daily_stress(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "daily_stress", {"start_date": start_date, "end_date": end_date}
        )

    async def get_daily_resilience(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "daily_resilience", {"start_date": start_date, "end_date": end_date}
        )

    async def get_daily_cardiovascular_age(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "daily_cardiovascular_age", {"start_date": start_date, "end_date": end_date}
        )

    # -- Detailed / session endpoints --

    async def get_sleep(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "sleep", {"start_date": start_date, "end_date": end_date}
        )

    async def get_sleep_time(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "sleep_time", {"start_date": start_date, "end_date": end_date}
        )

    async def get_sessions(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "session", {"start_date": start_date, "end_date": end_date}
        )

    async def get_workouts(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "workout", {"start_date": start_date, "end_date": end_date}
        )

    # -- Time-series endpoint --

    async def get_heart_rate(
        self, start_datetime: str | None = None, end_datetime: str | None = None
    ) -> list[dict]:
        """Heart rate uses datetime params (YYYY-MM-DDTHH:MM:SS), not date-only."""
        return await self._get_collection(
            "heartrate", {"start_datetime": start_datetime, "end_datetime": end_datetime}
        )

    # -- User & device endpoints --

    async def get_personal_info(self) -> dict:
        """Returns a single object, not a collection."""
        return await self._get("personal_info")

    async def get_ring_configuration(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "ring_configuration", {"start_date": start_date, "end_date": end_date}
        )

    async def get_rest_mode_period(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "rest_mode_period", {"start_date": start_date, "end_date": end_date}
        )

    async def get_vo2_max(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "vo2_max", {"start_date": start_date, "end_date": end_date}
        )

    # -- Tags --

    async def get_tags(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "tag", {"start_date": start_date, "end_date": end_date}
        )

    async def get_enhanced_tags(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> list[dict]:
        return await self._get_collection(
            "enhanced_tag", {"start_date": start_date, "end_date": end_date}
        )
