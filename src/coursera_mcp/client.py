"""Async HTTP client wrapping the Coursera Catalog API."""

from __future__ import annotations

from typing import Any

import httpx

from coursera_mcp.config import CourseraConfig


class CourseraError(Exception):
    """Raised when the Coursera API returns an error."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code


class CourseraClient:
    """Async client for the Coursera REST API.

    The Catalog API (courses, instructors, partners) is public.
    Authenticated endpoints require a CAUTH cookie.
    """

    def __init__(self, config: CourseraConfig) -> None:
        self._config = config
        cookies = {}
        if config.has_auth:
            cookies["CAUTH"] = config.cauth  # type: ignore[assignment]
        self._http = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=60.0,
            follow_redirects=True,
            cookies=cookies,
        )

    @property
    def has_auth(self) -> bool:
        return self._config.has_auth

    async def get(self, endpoint: str, **params: Any) -> dict[str, Any]:
        """Make a GET request to the Coursera API."""
        resp = await self._http.get(f"/{endpoint}", params=params)
        if resp.status_code >= 400:
            raise CourseraError(resp.status_code, f"Coursera API error: {resp.status_code} {resp.text[:200]}")
        return resp.json()

    async def post(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        """Make a POST request to the Coursera API."""
        resp = await self._http.post(
            f"/{endpoint}", json=body, params=params,
        )
        if resp.status_code >= 400:
            raise CourseraError(
                resp.status_code,
                f"Coursera API error: {resp.status_code}"
                f" {resp.text[:200]}",
            )
        return resp.json()

    async def aclose(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.aclose()
