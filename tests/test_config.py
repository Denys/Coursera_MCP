"""Tests for configuration loading."""

from __future__ import annotations

from coursera_mcp.config import CourseraConfig, load_config


def test_load_config_no_auth(monkeypatch):
    monkeypatch.delenv("COURSERA_CAUTH", raising=False)
    cfg = load_config()
    assert cfg.cauth is None
    assert not cfg.has_auth
    assert cfg.base_url == "https://api.coursera.org/api"


def test_load_config_with_cauth(monkeypatch):
    monkeypatch.setenv("COURSERA_CAUTH", "my_cauth_token")
    cfg = load_config()
    assert cfg.cauth == "my_cauth_token"
    assert cfg.has_auth


def test_config_default_base_url():
    cfg = CourseraConfig(cauth=None)
    assert cfg.base_url == "https://api.coursera.org/api"


def test_config_has_auth_false():
    cfg = CourseraConfig(cauth=None)
    assert not cfg.has_auth


def test_config_has_auth_true():
    cfg = CourseraConfig(cauth="token")
    assert cfg.has_auth
