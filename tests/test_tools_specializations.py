"""Tests for specialization tools."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.tools.specializations import get_specialization, list_specializations


@pytest.mark.asyncio
async def test_get_specialization(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {
                "id": "s1",
                "slug": "deep-learning",
                "name": "Deep Learning Specialization",
                "courseIds": ["c1", "c2", "c3"],
            },
        ],
    }
    result = await get_specialization(mock_client, specialization_id="s1")
    data = json.loads(result)
    assert data["name"] == "Deep Learning Specialization"
    assert len(data["course_ids"]) == 3


@pytest.mark.asyncio
async def test_get_specialization_not_found(mock_client):
    mock_client.get.return_value = {"elements": []}
    result = await get_specialization(mock_client, specialization_id="nonexistent")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_list_specializations(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "s1", "slug": "dl", "name": "Deep Learning"},
            {"id": "s2", "slug": "ml", "name": "Machine Learning"},
        ],
        "paging": {"total": 30},
    }
    result = await list_specializations(mock_client, start=0, limit=2)
    data = json.loads(result)
    assert data["total"] == 30
    assert len(data["specializations"]) == 2
