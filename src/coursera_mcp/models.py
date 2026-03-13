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
    def from_api(cls, data: dict[str, Any]) -> "Instructor":
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
    def from_api(cls, data: dict[str, Any]) -> "Partner":
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
    def from_api(cls, data: dict[str, Any]) -> "Course":
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
    def from_api(cls, data: dict[str, Any]) -> "Specialization":
        return cls.model_validate(data)


class CourseList(BaseModel):
    """Paginated list of courses."""

    total: int = 0
    courses: list[Course] = Field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "CourseList":
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
    def from_api(cls, data: dict[str, Any]) -> "SearchResult":
        elements = data.get("elements", [])
        paging = data.get("paging", {})
        return cls(
            total=paging.get("total", len(elements)),
            courses=[Course.from_api(e) for e in elements],
        )
