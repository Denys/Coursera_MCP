"""Specialization MCP tools."""

from __future__ import annotations

import json
from typing import Any

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import Specialization

SPECIALIZATION_FIELDS = "id,slug,name,description,logo,courseIds,partnerIds"


async def get_specialization(
    client: CourseraClient,
    *,
    specialization_id: str,
) -> str:
    """Get a specialization by its ID.

    Returns JSON with the specialization details including its courses.
    """
    data = await client.get(
        f"catalog.v1/s12ns/{specialization_id}",
        fields=SPECIALIZATION_FIELDS,
    )
    elements = data.get("elements", [])
    if not elements:
        return json.dumps(
            {"error": f"Specialization not found: {specialization_id}"},
            indent=2,
        )
    spec = Specialization.from_api(elements[0])
    return spec.model_dump_json(indent=2)


async def list_specializations(
    client: CourseraClient,
    *,
    start: int = 0,
    limit: int = 20,
) -> str:
    """List specializations from the Coursera catalog.

    Returns a paginated JSON list of specializations.
    """
    data = await client.get(
        "catalog.v1/s12ns",
        start=start,
        limit=limit,
        fields=SPECIALIZATION_FIELDS,
    )
    elements = data.get("elements", [])
    paging = data.get("paging", {})
    specs = [Specialization.from_api(e) for e in elements]
    return json.dumps(
        {
            "total": paging.get("total", len(specs)),
            "specializations": [s.model_dump() for s in specs],
        },
        indent=2,
    )
