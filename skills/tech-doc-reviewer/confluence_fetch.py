#!/usr/bin/env python3
"""
confluence_fetch.py — Bundled script for the confluence-doc-review skill.

Usage:
  python confluence_fetch.py page   <PAGE_ID>
  python confluence_fetch.py search <KEYWORD> [SPACE_KEY]
  python confluence_fetch.py list   <SPACE_KEY>

Authentication is read from environment variables:
  CONFLUENCE_URL        e.g. https://yourcompany.atlassian.net
  CONFLUENCE_EMAIL      e.g. you@company.com
  CONFLUENCE_API_TOKEN  your Atlassian API token

Output is JSON printed to stdout so the skill can parse it.
"""

import sys
import os
import json
from base64 import b64encode

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests library not installed. Run: pip install requests"}))
    sys.exit(1)

# ── Config from environment ────────────────────────────────────────────────────
BASE_URL    = os.environ.get("CONFLUENCE_URL", "").rstrip("/")
EMAIL       = os.environ.get("CONFLUENCE_EMAIL", "")
API_TOKEN   = os.environ.get("CONFLUENCE_API_TOKEN", "")

def validate_config():
    missing = [k for k, v in {
        "CONFLUENCE_URL": BASE_URL,
        "CONFLUENCE_EMAIL": EMAIL,
        "CONFLUENCE_API_TOKEN": API_TOKEN
    }.items() if not v]
    if missing:
        print(json.dumps({"error": f"Missing environment variables: {', '.join(missing)}"}))
        sys.exit(1)

def auth_headers():
    credentials = f"{EMAIL}:{API_TOKEN}"
    encoded = b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

# ── Confluence API helpers ─────────────────────────────────────────────────────
def get_page(page_id: str) -> dict:
    """Fetch a page by ID with body content."""
    url = f"{BASE_URL}/wiki/rest/api/content/{page_id}"
    params = {"expand": "body.storage,metadata.labels,version,space"}
    resp = requests.get(url, headers=auth_headers(), params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "id": data["id"],
        "title": data["title"],
        "space_key": data.get("space", {}).get("key", ""),
        "space_name": data.get("space", {}).get("name", ""),
        "version": data["version"]["number"],
        "last_modified": data["version"].get("when", ""),
        "author": data["version"].get("by", {}).get("displayName", ""),
        "body": data["body"]["storage"]["value"],
        "url": f"{BASE_URL}/wiki{data['_links']['webui']}",
    }


def search_pages(keyword: str, space_key: str = None, limit: int = 10) -> list:
    """Search pages by keyword using CQL."""
    cql = f'text ~ "{keyword}" AND type = page'
    if space_key:
        cql += f' AND space = "{space_key}"'
    url = f"{BASE_URL}/wiki/rest/api/content/search"
    params = {"cql": cql, "limit": limit}
    resp = requests.get(url, headers=auth_headers(), params=params)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    return [
        {
            "id": r["id"],
            "title": r["title"],
            "url": f"{BASE_URL}/wiki{r['_links']['webui']}"
        }
        for r in results
    ]


def list_pages(space_key: str, limit: int = 25) -> list:
    """List all pages in a Confluence space."""
    url = f"{BASE_URL}/wiki/rest/api/content"
    params = {
        "spaceKey": space_key,
        "type": "page",
        "limit": limit,
        "expand": "version"
    }
    resp = requests.get(url, headers=auth_headers(), params=params)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    return [
        {
            "id": r["id"],
            "title": r["title"],
            "version": r["version"]["number"],
            "url": f"{BASE_URL}/wiki{r['_links']['webui']}"
        }
        for r in results
    ]


# ── CLI entry point ────────────────────────────────────────────────────────────
def main():
    validate_config()

    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: python confluence_fetch.py [page|search|list] <args>"
        }))
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command == "page":
            page_id = sys.argv[2]
            result = get_page(page_id)

        elif command == "search":
            keyword   = sys.argv[2]
            space_key = sys.argv[3] if len(sys.argv) > 3 else None
            result = search_pages(keyword, space_key)

        elif command == "list":
            space_key = sys.argv[2]
            result = list_pages(space_key)

        else:
            result = {"error": f"Unknown command '{command}'. Use: page, search, list"}

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except requests.HTTPError as e:
        print(json.dumps({
            "error": f"Confluence API error {e.response.status_code}",
            "detail": e.response.text
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
