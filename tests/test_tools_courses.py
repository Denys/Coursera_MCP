"""Tests for course tools."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.tools.courses import get_course, get_course_by_slug, list_courses


@pytest.mark.asyncio
async def test_list_courses(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "abc", "slug": "ml", "name": "Machine Learning", "courseType": "v2.ondemand"},
            {"id": "def", "slug": "dl", "name": "Deep Learning", "courseType": "v2.ondemand"},
        ],
        "paging": {"total": 100},
    }
    result = await list_courses(mock_client, start=0, limit=2)
    data = json.loads(result)
    assert data["total"] == 100
    assert len(data["courses"]) == 2
    assert data["courses"][0]["name"] == "Machine Learning"


@pytest.mark.asyncio
async def test_get_course(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "abc", "slug": "ml", "name": "Machine Learning", "description": "Learn ML"},
        ],
    }
    result = await get_course(mock_client, course_id="abc")
    data = json.loads(result)
    assert data["id"] == "abc"
    assert data["name"] == "Machine Learning"


@pytest.mark.asyncio
async def test_get_course_not_found(mock_client):
    mock_client.get.return_value = {"elements": []}
    result = await get_course(mock_client, course_id="nonexistent")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_get_course_by_slug(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "abc", "slug": "machine-learning", "name": "Machine Learning"},
        ],
    }
    result = await get_course_by_slug(mock_client, slug="machine-learning")
    data = json.loads(result)
    assert data["slug"] == "machine-learning"


@pytest.mark.asyncio
async def test_get_course_by_slug_not_found(mock_client):
    mock_client.get.return_value = {"elements": []}
    result = await get_course_by_slug(mock_client, slug="nonexistent-course")
    data = json.loads(result)
    assert "error" in data
