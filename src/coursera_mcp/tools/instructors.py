"""Instructor-related MCP tools."""

from __future__ import annotations

import json
from typing import Any

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import Instructor

INSTRUCTOR_FIELDS = "id,firstName,lastName,title,department,photo"


async def get_instructor(
    client: CourseraClient,
    *,
    instructor_id: str,
) -> str:
    """Get an instructor by their ID.

    Returns JSON with the instructor details.
    """
    data = await client.get(
        f"catalog.v1/instructors/{instructor_id}",
        fields=INSTRUCTOR_FIELDS,
    )
    elements = data.get("elements", [])
    if not elements:
        return json.dumps({"error": f"Instructor not found: {instructor_id}"}, indent=2)
    instructor = Instructor.from_api(elements[0])
    return instructor.model_dump_json(indent=2)


async def list_instructors(
    client: CourseraClient,
    *,
    start: int = 0,
    limit: int = 20,
) -> str:
    """List instructors from the Coursera catalog.

    Returns a paginated JSON list of instructors.
    """
    data = await client.get(
        "catalog.v1/instructors",
        start=start,
        limit=limit,
        fields=INSTRUCTOR_FIELDS,
    )
    elements = data.get("elements", [])
    paging = data.get("paging", {})
    instructors = [Instructor.from_api(e) for e in elements]
    return json.dumps(
        {
            "total": paging.get("total", len(instructors)),
            "instructors": [i.model_dump() for i in instructors],
        },
        indent=2,
    )
