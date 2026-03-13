"""Tests for enrolled courses tools."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.tools.enrolled import list_enrolled_courses


@pytest.mark.asyncio
async def test_list_enrolled_courses(auth_mock_client):
    auth_mock_client.get.return_value = {
        "elements": [
            {"id": "user~course1", "courseId": "course1"},
            {"id": "user~course2", "courseId": "course2"},
        ],
        "linked": {
            "courses.v1": [
                {"id": "course1", "name": "Machine Learning", "slug": "ml"},
                {"id": "course2", "name": "Deep Learning", "slug": "deep-learning"},
            ],
        },
    }
    result = await list_enrolled_courses(auth_mock_client)
    data = json.loads(result)
    assert data["total"] == 2
    assert data["courses"][0]["courseId"] == "course1"
    assert data["courses"][0]["courseName"] == "Machine Learning"
    assert data["courses"][1]["courseSlug"] == "deep-learning"


@pytest.mark.asyncio
async def test_list_enrolled_courses_empty(auth_mock_client):
    auth_mock_client.get.return_value = {
        "elements": [],
        "linked": {"courses.v1": []},
    }
    result = await list_enrolled_courses(auth_mock_client)
    data = json.loads(result)
    assert data["total"] == 0
    assert data["courses"] == []


@pytest.mark.asyncio
async def test_list_enrolled_courses_no_auth(mock_client):
    result = await list_enrolled_courses(mock_client)
    data = json.loads(result)
    assert "error" in data
    assert "Authentication required" in data["error"]
