"""
mcp/confluence_server.py
Local MCP server for Confluence using FastMCP.

Run:
  python mcp/confluence_server.py

Requires:
  pip install fastmcp requests
  (or: uv pip install fastmcp requests)

Environment variables (set in .env or export before running):
  CONFLUENCE_URL        https://yourcompany.atlassian.net
  CONFLUENCE_EMAIL      you@yourcompany.com
  CONFLUENCE_API_TOKEN  <your Atlassian API token>
"""

import os
from base64 import b64encode

import requests
from fastmcp import FastMCP

# ── FastMCP server ─────────────────────────────────────────────────────────────
mcp = FastMCP(
    name="confluence-doc-review",
    instructions=(
        "Connects to Confluence and exposes tools to fetch, search, and list "
        "documentation pages. Used by the doc-reviewer agent to retrieve page "
        "content for quality review and scoring."
    ),
)

# ── Credentials ────────────────────────────────────────────────────────────────
_BASE_URL  = os.environ.get("CONFLUENCE_URL", "").rstrip("/")
_EMAIL     = os.environ.get("CONFLUENCE_EMAIL", "")
_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN", "")


def _headers() -> dict:
    missing = [k for k, v in {
        "CONFLUENCE_URL": _BASE_URL,
        "CONFLUENCE_EMAIL": _EMAIL,
        "CONFLUENCE_API_TOKEN": _API_TOKEN,
    }.items() if not v]
    if missing:
        raise RuntimeError(
            f"Missing environment variables: {', '.join(missing)}. "
            "Set them before starting the MCP server."
        )
    token = b64encode(f"{_EMAIL}:{_API_TOKEN}".encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ── Tools ──────────────────────────────────────────────────────────────────────

@mcp.tool
def get_page(page_id: str) -> dict:
    """
    Fetch a Confluence page by its ID.

    Returns the page title, raw HTML body, space, version, author,
    last modified date, and the direct page URL.
    Use this when you have a specific page ID or URL to review.

    Args:
        page_id: Numeric Confluence page ID (visible in the page URL after /pages/).
    """
    resp = requests.get(
        f"{_BASE_URL}/wiki/rest/api/content/{page_id}",
        headers=_headers(),
        params={"expand": "body.storage,metadata.labels,version,space"},
    )
    resp.raise_for_status()
    d = resp.json()
    return {
        "id":            d["id"],
        "title":         d["title"],
        "space_key":     d.get("space", {}).get("key", ""),
        "space_name":    d.get("space", {}).get("name", ""),
        "version":       d["version"]["number"],
        "last_modified": d["version"].get("when", ""),
        "author":        d["version"].get("by", {}).get("displayName", ""),
        "body":          d["body"]["storage"]["value"],
        "url":           f"{_BASE_URL}/wiki{d['_links']['webui']}",
    }


@mcp.tool
def search_pages(keyword: str, space_key: str = "", limit: int = 10) -> list[dict]:
    """
    Search Confluence pages by keyword using CQL.

    Returns a list of matching pages (id, title, url).
    Call get_page() on any result to retrieve the full body for review.

    Args:
        keyword:   Search term or phrase to look for in page content.
        space_key: Optional space key to narrow results (e.g. 'ENG', 'PLAT').
        limit:     Maximum number of results (default 10).
    """
    cql = f'text ~ "{keyword}" AND type = page'
    if space_key:
        cql += f' AND space = "{space_key}"'
    resp = requests.get(
        f"{_BASE_URL}/wiki/rest/api/content/search",
        headers=_headers(),
        params={"cql": cql, "limit": limit},
    )
    resp.raise_for_status()
    return [
        {
            "id":    r["id"],
            "title": r["title"],
            "url":   f"{_BASE_URL}/wiki{r['_links']['webui']}",
        }
        for r in resp.json().get("results", [])
    ]


@mcp.tool
def list_pages_in_space(space_key: str, limit: int = 25) -> list[dict]:
    """
    List all pages in a Confluence space.

    Returns id, title, version, and url for each page.
    Use this to see all docs in a space before deciding which ones to review.

    Args:
        space_key: Confluence space key (e.g. 'ENG', 'DOCS', 'PLAT').
        limit:     Maximum number of pages to return (default 25).
    """
    resp = requests.get(
        f"{_BASE_URL}/wiki/rest/api/content",
        headers=_headers(),
        params={
            "spaceKey": space_key,
            "type":     "page",
            "limit":    limit,
            "expand":   "version",
        },
    )
    resp.raise_for_status()
    return [
        {
            "id":      r["id"],
            "title":   r["title"],
            "version": r["version"]["number"],
            "url":     f"{_BASE_URL}/wiki{r['_links']['webui']}",
        }
        for r in resp.json().get("results", [])
    ]


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Confluence MCP server starting (stdio transport)...")
    print(f"  URL:   {_BASE_URL  or '⚠ CONFLUENCE_URL not set'}")
    print(f"  Email: {_EMAIL     or '⚠ CONFLUENCE_EMAIL not set'}")
    print()
    mcp.run()   # stdio — the transport GitHub Copilot uses
