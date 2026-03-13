"""Coursera MCP server entry point."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from coursera_mcp.client import CourseraClient, CourseraError
from coursera_mcp.config import load_config
from coursera_mcp.resources import read_course_resource, read_specialization_resource
from coursera_mcp.tools.courses import get_course, get_course_by_slug, list_courses
from coursera_mcp.tools.instructors import get_instructor, list_instructors
from coursera_mcp.tools.partners import get_partner, list_partners
from coursera_mcp.tools.search import search_courses
from coursera_mcp.tools.specializations import get_specialization, list_specializations

# ---------------------------------------------------------------------------
# App context
# ---------------------------------------------------------------------------

class _AppContext:
    def __init__(self, client: CourseraClient) -> None:
        self.client = client


@asynccontextmanager
async def _lifespan(server: FastMCP) -> AsyncIterator[_AppContext]:  # noqa: ARG001
    load_dotenv()
    config = load_config()
    client = CourseraClient(config)
    try:
        yield _AppContext(client)
    finally:
        await client.aclose()


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP("coursera", lifespan=_lifespan)


def _client() -> CourseraClient:
    """Return the CourseraClient from the active lifespan context."""
    return mcp.get_context().request_context.lifespan_context.client  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Course tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def coursera_list_courses(
    start: int = 0,
    limit: int = 20,
) -> str:
    """List courses from the Coursera catalog.

    Paginated: use *start* and *limit* to page through results.
    Returns JSON with a list of courses and total count.
    """
    return await list_courses(_client(), start=start, limit=limit)


@mcp.tool()
async def coursera_get_course(course_id: str) -> str:
    """Get detailed information about a specific Coursera course by its ID.

    Returns JSON with the full course details including description,
    instructors, partners, workload, and more.
    """
    return await get_course(_client(), course_id=course_id)


@mcp.tool()
async def coursera_get_course_by_slug(slug: str) -> str:
    """Look up a Coursera course by its URL slug.

    For example, the slug for https://www.coursera.org/learn/machine-learning
    is "machine-learning".
    Returns JSON with the full course details.
    """
    return await get_course_by_slug(_client(), slug=slug)


@mcp.tool()
async def coursera_search_courses(
    query: str,
    start: int = 0,
    limit: int = 20,
) -> str:
    """Search the Coursera course catalog by keyword.

    Returns JSON with matching courses and total count.
    Examples: "python programming", "data science", "deep learning".
    """
    return await search_courses(_client(), query=query, start=start, limit=limit)


# ---------------------------------------------------------------------------
# Instructor tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def coursera_get_instructor(instructor_id: str) -> str:
    """Get information about a Coursera instructor by their ID.

    Returns JSON with name, title, department, and photo.
    """
    return await get_instructor(_client(), instructor_id=instructor_id)


@mcp.tool()
async def coursera_list_instructors(
    start: int = 0,
    limit: int = 20,
) -> str:
    """List instructors from the Coursera catalog.

    Paginated: use *start* and *limit* to page through results.
    Returns JSON with a list of instructors and total count.
    """
    return await list_instructors(_client(), start=start, limit=limit)


# ---------------------------------------------------------------------------
# Partner tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def coursera_get_partner(partner_id: str) -> str:
    """Get information about a Coursera partner (university/organization).

    Returns JSON with name, description, and homepage link.
    """
    return await get_partner(_client(), partner_id=partner_id)


@mcp.tool()
async def coursera_list_partners(
    start: int = 0,
    limit: int = 20,
) -> str:
    """List partners (universities and organizations) from the Coursera catalog.

    Paginated: use *start* and *limit* to page through results.
    Returns JSON with a list of partners and total count.
    """
    return await list_partners(_client(), start=start, limit=limit)


# ---------------------------------------------------------------------------
# Specialization tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def coursera_get_specialization(specialization_id: str) -> str:
    """Get information about a Coursera specialization (series of courses).

    Returns JSON with name, description, and the list of course IDs.
    """
    return await get_specialization(_client(), specialization_id=specialization_id)


@mcp.tool()
async def coursera_list_specializations(
    start: int = 0,
    limit: int = 20,
) -> str:
    """List specializations from the Coursera catalog.

    Paginated: use *start* and *limit* to page through results.
    Returns JSON with a list of specializations and total count.
    """
    return await list_specializations(_client(), start=start, limit=limit)


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

@mcp.resource("coursera://course/{course_id}")
async def coursera_course_resource(course_id: str) -> str:
    """Browse a Coursera course as a resource.

    URI: ``coursera://course/{course_id}``
    Returns JSON with the full course details.
    """
    return await read_course_resource(_client(), course_id)


@mcp.resource("coursera://specialization/{specialization_id}")
async def coursera_specialization_resource(specialization_id: str) -> str:
    """Browse a Coursera specialization as a resource.

    URI: ``coursera://specialization/{specialization_id}``
    Returns JSON with the specialization details.
    """
    return await read_specialization_resource(_client(), specialization_id)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the Coursera MCP server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
