"""Partner (university / organization) MCP tools."""

from __future__ import annotations

import json
from typing import Any

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import Partner

PARTNER_FIELDS = "id,name,shortName,description,links,logo"


async def get_partner(
    client: CourseraClient,
    *,
    partner_id: str,
) -> str:
    """Get a partner (university/organization) by their ID.

    Returns JSON with the partner details.
    """
    data = await client.get(
        f"catalog.v1/partners/{partner_id}",
        fields=PARTNER_FIELDS,
    )
    elements = data.get("elements", [])
    if not elements:
        return json.dumps({"error": f"Partner not found: {partner_id}"}, indent=2)
    partner = Partner.from_api(elements[0])
    return partner.model_dump_json(indent=2)


async def list_partners(
    client: CourseraClient,
    *,
    start: int = 0,
    limit: int = 20,
) -> str:
    """List partners (universities/organizations) from the catalog.

    Returns a paginated JSON list of partners.
    """
    data = await client.get(
        "catalog.v1/partners",
        start=start,
        limit=limit,
        fields=PARTNER_FIELDS,
    )
    elements = data.get("elements", [])
    paging = data.get("paging", {})
    partners = [Partner.from_api(e) for e in elements]
    return json.dumps(
        {
            "total": paging.get("total", len(partners)),
            "partners": [p.model_dump() for p in partners],
        },
        indent=2,
    )
