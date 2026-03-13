"""MCP resource handlers for browsing Coursera via URI scheme."""

from __future__ import annotations

import json

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import Course, Specialization
from coursera_mcp.tools.courses import COURSE_FIELDS
from coursera_mcp.tools.specializations import SPECIALIZATION_FIELDS


async def read_course_resource(client: CourseraClient, course_id: str) -> str:
    """Return JSON course details for ``coursera://course/{course_id}``."""
    data = await client.get(
        f"catalog.v1/courses/{course_id}",
        fields=COURSE_FIELDS,
    )
    elements = data.get("elements", [])
    if not elements:
        return json.dumps({"error": f"Course not found: {course_id}"})
    course = Course.from_api(elements[0])
    return course.model_dump_json(indent=2)


async def read_specialization_resource(client: CourseraClient, specialization_id: str) -> str:
    """Return JSON specialization details for ``coursera://specialization/{id}``."""
    data = await client.get(
        f"catalog.v1/s12ns/{specialization_id}",
        fields=SPECIALIZATION_FIELDS,
    )
    elements = data.get("elements", [])
    if not elements:
        return json.dumps({"error": f"Specialization not found: {specialization_id}"})
    spec = Specialization.from_api(elements[0])
    return spec.model_dump_json(indent=2)
