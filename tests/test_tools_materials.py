"""Tests for course materials tools."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.tools.materials import (
    get_course_materials,
    get_lecture_video,
    get_supplement,
)


@pytest.mark.asyncio
async def test_get_course_materials(auth_mock_client):
    auth_mock_client.get.return_value = {
        "elements": [{"id": "course123", "moduleIds": ["mod1"]}],
        "linked": {
            "onDemandCourseMaterialModules.v1": [
                {
                    "id": "mod1",
                    "name": "Week 1",
                    "slug": "week-1",
                    "lessonIds": ["les1"],
                    "optional": False,
                },
            ],
            "onDemandCourseMaterialLessons.v1": [
                {
                    "id": "les1",
                    "name": "Intro",
                    "slug": "intro",
                    "elementIds": ["item1"],
                    "trackId": "core",
                },
            ],
            "onDemandCourseMaterialItems.v2": [
                {
                    "id": "item1",
                    "name": "Welcome Video",
                    "slug": "welcome",
                    "contentSummary": {
                        "typeName": "lecture",
                        "definition": {"videoId": "vid1"},
                    },
                    "isLocked": False,
                    "trackId": "core",
                },
            ],
        },
    }
    result = await get_course_materials(auth_mock_client, course_slug="ml-course")
    data = json.loads(result)
    assert data["course_id"] == "course123"
    assert len(data["modules"]) == 1
    assert data["modules"][0]["name"] == "Week 1"
    assert len(data["lessons"]) == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["type_name"] == "lecture"


@pytest.mark.asyncio
async def test_get_course_materials_not_found(auth_mock_client):
    auth_mock_client.get.return_value = {"elements": [], "linked": {}}
    result = await get_course_materials(auth_mock_client, course_slug="nonexistent")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_get_course_materials_no_auth(mock_client):
    result = await get_course_materials(mock_client, course_slug="ml-course")
    data = json.loads(result)
    assert "error" in data
    assert "Authentication required" in data["error"]


@pytest.mark.asyncio
async def test_get_lecture_video(auth_mock_client):
    auth_mock_client.get.return_value = {
        "linked": {
            "onDemandVideos.v1": [
                {
                    "id": "vid1",
                    "sources": {
                        "byResolution": {
                            "720p": {"mp4VideoUrl": "https://example.com/720p.mp4"},
                            "360p": {"mp4VideoUrl": "https://example.com/360p.mp4"},
                        },
                    },
                    "subtitles": {"en": "https://example.com/en.srt"},
                },
            ],
        },
    }
    result = await get_lecture_video(auth_mock_client, course_id="c1", video_id="v1")
    data = json.loads(result)
    assert "720p" in data["sources"]
    assert data["subtitles"]["en"] == "https://example.com/en.srt"


@pytest.mark.asyncio
async def test_get_lecture_video_not_found(auth_mock_client):
    auth_mock_client.get.return_value = {"linked": {"onDemandVideos.v1": []}}
    result = await get_lecture_video(auth_mock_client, course_id="c1", video_id="v1")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_get_lecture_video_no_auth(mock_client):
    result = await get_lecture_video(mock_client, course_id="c1", video_id="v1")
    data = json.loads(result)
    assert "Authentication required" in data["error"]


@pytest.mark.asyncio
async def test_get_supplement(auth_mock_client):
    auth_mock_client.get.return_value = {
        "linked": {
            "openCourseAssets.v1": [
                {
                    "id": "asset1",
                    "typeName": "cml",
                    "definition": {
                        "dtdId": "cml",
                        "value": "<co-content>Reading</co-content>",
                    },
                },
            ],
        },
    }
    result = await get_supplement(auth_mock_client, course_id="c1", element_id="e1")
    data = json.loads(result)
    assert data["id"] == "asset1"
    assert data["type_name"] == "cml"


@pytest.mark.asyncio
async def test_get_supplement_not_found(auth_mock_client):
    auth_mock_client.get.return_value = {"linked": {"openCourseAssets.v1": []}}
    result = await get_supplement(auth_mock_client, course_id="c1", element_id="e1")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_get_supplement_no_auth(mock_client):
    result = await get_supplement(mock_client, course_id="c1", element_id="e1")
    data = json.loads(result)
    assert "Authentication required" in data["error"]
