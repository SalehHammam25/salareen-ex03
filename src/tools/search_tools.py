"""Web search wrapper for the Research Agent.

Real search (SerperDev) is optional and activated only when SERPER_API_KEY
is present in the environment.  Tests can inject a fake provider via the
*provider* parameter — no network calls are required.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Callable, Sequence


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    source: str = field(default="")


# Type alias for a search-provider callable.
SearchProvider = Callable[[str, int], list[SearchResult]]


def _serper_provider(query: str, max_results: int) -> list[SearchResult]:
    """Live search via SerperDev API (requires SERPER_API_KEY)."""
    import json
    import urllib.request

    api_key = os.environ.get("SERPER_API_KEY", "")
    if not api_key:
        raise EnvironmentError("SERPER_API_KEY is not set")

    payload = json.dumps({"q": query, "num": max_results}).encode()
    req = urllib.request.Request(
        "https://google.serper.dev/search",
        data=payload,
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    results = []
    for item in data.get("organic", [])[:max_results]:
        results.append(
            SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source=item.get("source", ""),
            )
        )
    return results


def search(
    query: str,
    max_results: int = 5,
    *,
    provider: SearchProvider | None = None,
) -> list[SearchResult]:
    """Run a search and return up to *max_results* SearchResult objects.

    If *provider* is given it is used as-is (useful for tests).
    Otherwise falls back to the SerperDev live provider.
    """
    if provider is not None:
        return provider(query, max_results)
    return _serper_provider(query, max_results)


def format_results_as_markdown(results: Sequence[SearchResult]) -> str:
    """Render a list of SearchResult objects as a Markdown bullet list."""
    if not results:
        return "_No results found._\n"
    lines: list[str] = []
    for r in results:
        source_tag = f" ({r.source})" if r.source else ""
        lines.append(f"- **[{r.title}]({r.url})**{source_tag}  ")
        lines.append(f"  {r.snippet}")
        lines.append("")
    return "\n".join(lines)
