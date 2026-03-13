"""Tests for MCP resource handlers."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.resources import read_course_resource, read_specialization_resource


@pytest.mark.asyncio
async def test_read_course_resource(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "abc", "slug": "ml", "name": "Machine Learning", "description": "Learn ML"},
        ],
    }
    result = await read_course_resource(mock_client, "abc")
    data = json.loads(result)
    assert data["id"] == "abc"
    assert data["name"] == "Machine Learning"


@pytest.mark.asyncio
async def test_read_course_resource_not_found(mock_client):
    mock_client.get.return_value = {"elements": []}
    result = await read_course_resource(mock_client, "nonexistent")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_read_specialization_resource(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "s1", "slug": "dl", "name": "Deep Learning", "courseIds": ["c1", "c2"]},
        ],
    }
    result = await read_specialization_resource(mock_client, "s1")
    data = json.loads(result)
    assert data["id"] == "s1"
    assert data["name"] == "Deep Learning"


@pytest.mark.asyncio
async def test_read_specialization_resource_not_found(mock_client):
    mock_client.get.return_value = {"elements": []}
    result = await read_specialization_resource(mock_client, "nonexistent")
    data = json.loads(result)
    assert "error" in data
