"""Tools for listing enrolled courses (requires CAUTH authentication)."""

from __future__ import annotations

import json

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import EnrolledCourse

AUTH_ERROR = json.dumps(
    {"error": "Authentication required. Set the COURSERA_CAUTH environment variable."},
    indent=2,
)


async def list_enrolled_courses(client: CourseraClient) -> str:
    """List courses the authenticated user is enrolled in.

    Returns JSON with a list of enrolled courses.
    Requires CAUTH authentication.
    """
    if not client.has_auth:
        return AUTH_ERROR

    data = await client.get(
        "memberships.v1",
        q="me",
        includes="courseId,courses.v1",
        fields="courseId,courses.v1(name,slug)",
        showHidden="true",
        filter="current,preEnrolled",
    )

    memberships = data.get("elements", [])
    linked = data.get("linked", {})
    courses_list = linked.get("courses.v1", [])
    courses_map = {c["id"]: c for c in courses_list}

    enrolled = [
        EnrolledCourse.from_membership(m, courses_map)
        for m in memberships
    ]

    result = {
        "total": len(enrolled),
        "courses": [e.model_dump(by_alias=True) for e in enrolled],
    }
    return json.dumps(result, indent=2)
