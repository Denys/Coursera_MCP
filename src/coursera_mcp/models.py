"""Pydantic models for Coursera API responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Instructor(BaseModel):
    """An instructor on Coursera."""

    id: str = ""
    first_name: str = Field(default="", alias="firstName")
    last_name: str = Field(default="", alias="lastName")
    title: str = ""
    department: str = ""
    photo: str = ""

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Instructor:
        return cls.model_validate(data)


class Partner(BaseModel):
    """A university or organization on Coursera."""

    id: str = ""
    name: str = ""
    short_name: str = Field(default="", alias="shortName")
    description: str = ""
    homepage_link: str = Field(default="", alias="links.homepage")
    logo: str = ""

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Partner:
        return cls.model_validate(data)


class Course(BaseModel):
    """A course on Coursera."""

    id: str = ""
    slug: str = ""
    name: str = ""
    course_type: str = Field(default="", alias="courseType")
    description: str = ""
    photo_url: str = Field(default="", alias="photoUrl")
    workload: str = ""
    start_date: str | None = Field(default=None, alias="startDate")
    preview_link: str = Field(default="", alias="previewLink")
    partner_ids: list[str] = Field(default_factory=list, alias="partnerIds")
    instructor_ids: list[str] = Field(default_factory=list, alias="instructorIds")
    domain_types: list[dict[str, str]] = Field(default_factory=list, alias="domainTypes")

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Course:
        return cls.model_validate(data)


class Specialization(BaseModel):
    """A specialization (series of courses) on Coursera."""

    id: str = ""
    slug: str = ""
    name: str = ""
    description: str = ""
    logo: str = ""
    course_ids: list[str] = Field(default_factory=list, alias="courseIds")
    partner_ids: list[str] = Field(default_factory=list, alias="partnerIds")

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Specialization:
        return cls.model_validate(data)


# ---------------------------------------------------------------------------
# Enrolled content models (require CAUTH authentication)
# ---------------------------------------------------------------------------


class EnrolledCourse(BaseModel):
    """A course the user is enrolled in."""

    course_id: str = Field(default="", alias="courseId")
    course_name: str = Field(default="", alias="courseName")
    course_slug: str = Field(default="", alias="courseSlug")

    model_config = {"populate_by_name": True}

    @classmethod
    def from_membership(
        cls,
        membership: dict[str, Any],
        courses_map: dict[str, dict[str, Any]],
    ) -> EnrolledCourse:
        course_id = membership.get("courseId", "")
        course_data = courses_map.get(course_id, {})
        return cls(
            course_id=course_id,
            course_name=course_data.get("name", ""),
            course_slug=course_data.get("slug", ""),
        )


class CourseMaterialItem(BaseModel):
    """An item (lecture, quiz, assignment, etc.) within a lesson."""

    id: str = ""
    name: str = ""
    slug: str = ""
    type_name: str = Field(default="", alias="typeName")
    is_locked: bool = Field(default=False, alias="isLocked")
    track_id: str = Field(default="", alias="trackId")

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CourseMaterialItem:
        content_summary = data.get("contentSummary", {})
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            slug=data.get("slug", ""),
            type_name=content_summary.get("typeName", ""),
            is_locked=data.get("isLocked", False),
            track_id=data.get("trackId", ""),
        )


class CourseMaterialLesson(BaseModel):
    """A lesson within a module."""

    id: str = ""
    name: str = ""
    slug: str = ""
    element_ids: list[str] = Field(default_factory=list, alias="elementIds")
    track_id: str = Field(default="", alias="trackId")

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CourseMaterialLesson:
        return cls.model_validate(data)


class CourseMaterialModule(BaseModel):
    """A module within a course."""

    id: str = ""
    name: str = ""
    slug: str = ""
    description: str = ""
    lesson_ids: list[str] = Field(default_factory=list, alias="lessonIds")
    optional: bool = False

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CourseMaterialModule:
        return cls.model_validate(data)


class CourseMaterials(BaseModel):
    """Full course materials structure (modules, lessons, items)."""

    course_id: str = ""
    modules: list[CourseMaterialModule] = Field(default_factory=list)
    lessons: list[CourseMaterialLesson] = Field(default_factory=list)
    items: list[CourseMaterialItem] = Field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CourseMaterials:
        elements = data.get("elements", [])
        linked = data.get("linked", {})
        course_id = elements[0]["id"] if elements else ""
        modules = [
            CourseMaterialModule.from_api(m)
            for m in linked.get("onDemandCourseMaterialModules.v1", [])
        ]
        lessons = [
            CourseMaterialLesson.from_api(les)
            for les in linked.get("onDemandCourseMaterialLessons.v1", [])
        ]
        items = [
            CourseMaterialItem.from_api(i)
            for i in linked.get("onDemandCourseMaterialItems.v2", [])
        ]
        return cls(course_id=course_id, modules=modules, lessons=lessons, items=items)


class LectureVideo(BaseModel):
    """Video sources and subtitles for a lecture."""

    video_id: str = ""
    sources: dict[str, str] = Field(default_factory=dict)
    subtitles: dict[str, str] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> LectureVideo:
        linked = data.get("linked", {})
        videos = linked.get("onDemandVideos.v1", [])
        if not videos:
            return cls()
        video = videos[0]
        sources = {}
        by_res = video.get("sources", {}).get("byResolution", {})
        for res, info in by_res.items():
            if isinstance(info, dict) and "mp4VideoUrl" in info:
                sources[res] = info["mp4VideoUrl"]
        subtitles = video.get("subtitles", {})
        return cls(video_id=video.get("id", ""), sources=sources, subtitles=subtitles)


class CourseGrade(BaseModel):
    """Grade information for a course."""

    course_id: str = ""
    overall_grade: float = 0.0
    is_passed: bool = False
    item_grades: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CourseGrade:
        elements = data.get("elements", [])
        if not elements:
            return cls()
        elem = elements[0]
        return cls(
            course_id=elem.get("id", ""),
            overall_grade=elem.get("overallGrade", 0.0),
            is_passed=elem.get("isPassed", False),
            item_grades=elem.get("itemGrades", {}),
        )


class Supplement(BaseModel):
    """A supplement (reading/resource) within a course."""

    id: str = ""
    type_name: str = ""
    definition: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Supplement:
        linked = data.get("linked", {})
        assets = linked.get("openCourseAssets.v1", [])
        if not assets:
            return cls()
        asset = assets[0]
        return cls(
            id=asset.get("id", ""),
            type_name=asset.get("typeName", ""),
            definition=asset.get("definition", {}),
        )


class CourseList(BaseModel):
    """Paginated list of courses."""

    total: int = 0
    courses: list[Course] = Field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CourseList:
        elements = data.get("elements", [])
        paging = data.get("paging", {})
        return cls(
            total=paging.get("total", len(elements)),
            courses=[Course.from_api(e) for e in elements],
        )


class SearchResult(BaseModel):
    """Result from a course search."""

    total: int = 0
    courses: list[Course] = Field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> SearchResult:
        elements = data.get("elements", [])
        paging = data.get("paging", {})
        return cls(
            total=paging.get("total", len(elements)),
            courses=[Course.from_api(e) for e in elements],
        )
