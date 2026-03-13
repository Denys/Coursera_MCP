"""Tools for accessing course grades (requires CAUTH authentication)."""

from __future__ import annotations

import json

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import CourseGrade

AUTH_ERROR = json.dumps(
    {"error": "Authentication required. Set the COURSERA_CAUTH environment variable."},
    indent=2,
)


async def get_course_grades(
    client: CourseraClient,
    *,
    course_id: str,
) -> str:
    """Get grade information for an enrolled course.

    Returns JSON with overall grade, passing status, and item grades.
    Requires CAUTH authentication.
    """
    if not client.has_auth:
        return AUTH_ERROR

    data = await client.get(f"onDemandCourseGrades.v1/{course_id}")

    grade = CourseGrade.from_api(data)
    if not grade.course_id:
        return json.dumps(
            {"error": f"Grades not found for course: {course_id}"},
            indent=2,
        )

    return grade.model_dump_json(indent=2)
