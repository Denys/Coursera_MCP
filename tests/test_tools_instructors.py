"""Tests for instructor tools."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.tools.instructors import get_instructor, list_instructors


@pytest.mark.asyncio
async def test_get_instructor(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "123", "firstName": "Andrew", "lastName": "Ng", "title": "Professor"},
        ],
    }
    result = await get_instructor(mock_client, instructor_id="123")
    data = json.loads(result)
    assert data["first_name"] == "Andrew"
    assert data["last_name"] == "Ng"


@pytest.mark.asyncio
async def test_get_instructor_not_found(mock_client):
    mock_client.get.return_value = {"elements": []}
    result = await get_instructor(mock_client, instructor_id="nonexistent")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_list_instructors(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "1", "firstName": "Andrew", "lastName": "Ng"},
            {"id": "2", "firstName": "Geoffrey", "lastName": "Hinton"},
        ],
        "paging": {"total": 200},
    }
    result = await list_instructors(mock_client, start=0, limit=2)
    data = json.loads(result)
    assert data["total"] == 200
    assert len(data["instructors"]) == 2
