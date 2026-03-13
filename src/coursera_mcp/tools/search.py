"""Search MCP tools for Coursera courses."""

from __future__ import annotations

from typing import Any

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import SearchResult
from coursera_mcp.tools.courses import COURSE_FIELDS


async def search_courses(
    client: CourseraClient,
    *,
    query: str,
    start: int = 0,
    limit: int = 20,
) -> str:
    """Search the Coursera catalog by keyword.

    Returns JSON with matching courses.
    """
    data = await client.get(
        "catalog.v1/courses",
        q="search",
        query=query,
        start=start,
        limit=limit,
        fields=COURSE_FIELDS,
    )
    result = SearchResult.from_api(data)
    return result.model_dump_json(indent=2)
