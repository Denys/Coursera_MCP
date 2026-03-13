"""Tests for partner tools."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.tools.partners import get_partner, list_partners


@pytest.mark.asyncio
async def test_get_partner(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "1", "name": "Stanford University", "shortName": "stanford"},
        ],
    }
    result = await get_partner(mock_client, partner_id="1")
    data = json.loads(result)
    assert data["name"] == "Stanford University"


@pytest.mark.asyncio
async def test_get_partner_not_found(mock_client):
    mock_client.get.return_value = {"elements": []}
    result = await get_partner(mock_client, partner_id="nonexistent")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_list_partners(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "1", "name": "Stanford University"},
            {"id": "2", "name": "MIT"},
        ],
        "paging": {"total": 50},
    }
    result = await list_partners(mock_client, start=0, limit=2)
    data = json.loads(result)
    assert data["total"] == 50
    assert len(data["partners"]) == 2
