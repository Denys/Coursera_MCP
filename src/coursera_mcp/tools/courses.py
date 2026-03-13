"""Course-related MCP tools: list, get, get by slug."""

from __future__ import annotations

import json

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import Course, CourseList

COURSE_FIELDS = (
    "id,slug,name,courseType,description,photoUrl,workload,"
    "startDate,previewLink,partnerIds,instructorIds,domainTypes"
)


async def list_courses(
    client: CourseraClient,
    *,
    start: int = 0,
    limit: int = 20,
) -> str:
    """List courses from the Coursera catalog.

    Returns a paginated JSON list of courses.
    """
    data = await client.get(
        "catalog.v1/courses",
        start=start,
        limit=limit,
        fields=COURSE_FIELDS,
    )
    result = CourseList.from_api(data)
    return result.model_dump_json(indent=2)


async def get_course(
    client: CourseraClient,
    *,
    course_id: str,
) -> str:
    """Get a single course by its ID.

    Returns JSON with the full course details.
    """
    data = await client.get(
        f"catalog.v1/courses/{course_id}",
        fields=COURSE_FIELDS,
    )
    elements = data.get("elements", [])
    if not elements:
        return json.dumps({"error": f"Course not found: {course_id}"}, indent=2)
    course = Course.from_api(elements[0])
    return course.model_dump_json(indent=2)


async def get_course_by_slug(
    client: CourseraClient,
    *,
    slug: str,
) -> str:
    """Get a course by its URL slug (e.g. "machine-learning").

    Returns JSON with the full course details.
    """
    data = await client.get(
        "catalog.v1/courses",
        q="search",
        query=slug,
        fields=COURSE_FIELDS,
        limit=5,
    )
    elements = data.get("elements", [])
    # Try to find an exact slug match first
    for elem in elements:
        if elem.get("slug") == slug:
            course = Course.from_api(elem)
            return course.model_dump_json(indent=2)
    # Fall back to first result if no exact match
    if elements:
        course = Course.from_api(elements[0])
        return course.model_dump_json(indent=2)
    return json.dumps({"error": f"Course not found for slug: {slug}"}, indent=2)
