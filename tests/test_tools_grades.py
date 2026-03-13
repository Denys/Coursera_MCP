"""Tests for course grades tools."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.tools.grades import get_course_grades


@pytest.mark.asyncio
async def test_get_course_grades(auth_mock_client):
    auth_mock_client.get.return_value = {
        "elements": [
            {
                "id": "course123",
                "overallGrade": 0.95,
                "isPassed": True,
                "itemGrades": {"item1": {"grade": 1.0}, "item2": {"grade": 0.9}},
            },
        ],
    }
    result = await get_course_grades(auth_mock_client, course_id="course123")
    data = json.loads(result)
    assert data["course_id"] == "course123"
    assert data["overall_grade"] == 0.95
    assert data["is_passed"] is True
    assert "item1" in data["item_grades"]


@pytest.mark.asyncio
async def test_get_course_grades_not_found(auth_mock_client):
    auth_mock_client.get.return_value = {"elements": []}
    result = await get_course_grades(auth_mock_client, course_id="nonexistent")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_get_course_grades_no_auth(mock_client):
    result = await get_course_grades(mock_client, course_id="course123")
    data = json.loads(result)
    assert "error" in data
    assert "Authentication required" in data["error"]
