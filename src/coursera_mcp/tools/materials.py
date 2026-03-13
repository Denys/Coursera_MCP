"""Tools for accessing course materials, lectures, and supplements (requires CAUTH)."""

from __future__ import annotations

import json

from coursera_mcp.client import CourseraClient
from coursera_mcp.models import CourseMaterials, LectureVideo, Supplement

AUTH_ERROR = json.dumps(
    {"error": "Authentication required. Set the COURSERA_CAUTH environment variable."},
    indent=2,
)

MATERIALS_FIELDS = (
    "onDemandCourseMaterialModules.v1(name,slug,description,timeCommitment,lessonIds,optional,learningObjectives),"
    "onDemandCourseMaterialLessons.v1(name,slug,timeCommitment,elementIds,optional,trackId),"
    "onDemandCourseMaterialItems.v2(name,slug,timeCommitment,contentSummary,isLocked,lockableByItem,"
    "itemLockedReasonCode,trackId,lockedStatus,itemLockSummary)"
)

MATERIALS_INCLUDES = (
    "modules,lessons,passableItemGroups,passableItemGroupChoices,"
    "passableLessonElements,items,tracks,gradePolicy"
)


async def get_course_materials(
    client: CourseraClient,
    *,
    course_slug: str,
) -> str:
    """Get the full course structure (modules, lessons, items) for a course.

    Returns JSON with modules, lessons, and items including lecture types.
    Requires CAUTH authentication.
    """
    if not client.has_auth:
        return AUTH_ERROR

    data = await client.get(
        "onDemandCourseMaterials.v2/",
        q="slug",
        slug=course_slug,
        includes=MATERIALS_INCLUDES,
        fields=MATERIALS_FIELDS,
        showLockedItems="true",
    )

    elements = data.get("elements", [])
    if not elements:
        return json.dumps(
            {"error": f"Course materials not found for: {course_slug}"},
            indent=2,
        )

    materials = CourseMaterials.from_api(data)
    return materials.model_dump_json(indent=2)


async def get_lecture_video(
    client: CourseraClient,
    *,
    course_id: str,
    video_id: str,
) -> str:
    """Get video URLs and subtitles for a specific lecture.

    The course_id and video_id are combined as course_id~video_id.
    Returns JSON with video sources (by resolution) and subtitle URLs.
    Requires CAUTH authentication.
    """
    if not client.has_auth:
        return AUTH_ERROR

    data = await client.get(
        f"onDemandLectureVideos.v1/{course_id}~{video_id}",
        includes="video",
        fields="onDemandVideos.v1(sources,subtitles,subtitlesVtt,subtitlesTxt)",
    )

    video = LectureVideo.from_api(data)
    if not video.sources:
        return json.dumps(
            {"error": f"Lecture video not found: {course_id}~{video_id}"},
            indent=2,
        )

    return video.model_dump_json(indent=2)


async def get_supplement(
    client: CourseraClient,
    *,
    course_id: str,
    element_id: str,
) -> str:
    """Get a supplement (reading/resource) for a course item.

    Returns JSON with the supplement content definition.
    Requires CAUTH authentication.
    """
    if not client.has_auth:
        return AUTH_ERROR

    data = await client.get(
        f"onDemandSupplements.v1/{course_id}~{element_id}",
        includes="asset",
        fields="openCourseAssets.v1(typeName),openCourseAssets.v1(definition)",
    )

    supplement = Supplement.from_api(data)
    if not supplement.id:
        return json.dumps(
            {"error": f"Supplement not found: {course_id}~{element_id}"},
            indent=2,
        )

    return supplement.model_dump_json(indent=2)
