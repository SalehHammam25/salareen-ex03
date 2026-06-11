"""Tests for src/tools/search_tools.py — no real network calls."""

from __future__ import annotations

import pytest

from src.tools.search_tools import (
    SearchResult,
    format_results_as_markdown,
    search,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _fake_provider(query: str, max_results: int) -> list[SearchResult]:
    """Return synthetic results without any network access."""
    return [
        SearchResult(
            title=f"Result {i}: {query}",
            url=f"https://example.com/{i}",
            snippet=f"Snippet for result {i} about '{query}'.",
            source="example.com",
        )
        for i in range(1, min(max_results, 3) + 1)
    ]


# ---------------------------------------------------------------------------
# SearchResult dataclass
# ---------------------------------------------------------------------------

def test_search_result_fields():
    r = SearchResult(title="T", url="https://x.com", snippet="S", source="x.com")
    assert r.title == "T"
    assert r.url == "https://x.com"
    assert r.snippet == "S"
    assert r.source == "x.com"


def test_search_result_source_defaults_to_empty():
    r = SearchResult(title="T", url="u", snippet="s")
    assert r.source == ""


# ---------------------------------------------------------------------------
# search() with injected provider
# ---------------------------------------------------------------------------

def test_search_returns_list_of_search_results():
    results = search("HITL", provider=_fake_provider)
    assert isinstance(results, list)
    assert all(isinstance(r, SearchResult) for r in results)


def test_search_respects_max_results():
    results = search("test", max_results=2, provider=_fake_provider)
    assert len(results) <= 2


def test_search_passes_query_to_provider():
    results = search("human in the loop", provider=_fake_provider)
    assert any("human in the loop" in r.title for r in results)


def test_search_with_empty_provider_returns_empty():
    results = search("q", provider=lambda q, n: [])
    assert results == []


def test_search_no_real_network_when_provider_given(monkeypatch):
    """Ensure the live _serper_provider is never called when provider= is set."""
    import src.tools.search_tools as st

    def _boom(query, max_results):
        raise AssertionError("Real network call was made!")

    monkeypatch.setattr(st, "_serper_provider", _boom)
    results = search("q", provider=_fake_provider)
    assert len(results) > 0


# ---------------------------------------------------------------------------
# format_results_as_markdown
# ---------------------------------------------------------------------------

def test_format_empty_results():
    md = format_results_as_markdown([])
    assert "No results" in md


def test_format_includes_title_and_url():
    results = [SearchResult(title="Hello", url="https://a.com", snippet="A snippet")]
    md = format_results_as_markdown(results)
    assert "Hello" in md
    assert "https://a.com" in md


def test_format_includes_snippet():
    results = [SearchResult(title="T", url="u", snippet="my snippet")]
    md = format_results_as_markdown(results)
    assert "my snippet" in md


def test_format_includes_source_when_present():
    results = [SearchResult(title="T", url="u", snippet="s", source="site.com")]
    md = format_results_as_markdown(results)
    assert "site.com" in md


def test_format_multiple_results_are_all_present():
    results = _fake_provider("ai", 3)
    md = format_results_as_markdown(results)
    for r in results:
        assert r.title in md
        assert r.url in md
