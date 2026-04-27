# Confluence Doc Reviewer — GitHub Copilot Agent

Reviews Confluence technical documentation and scores it across 10 quality
criteria using a local FastMCP server, a GitHub Copilot skill, and a custom agent.

---

## Project Structure

```
confluence-doc-reviewer/
│
├── mcp/
│   └── confluence_server.py        # Local FastMCP server (Confluence API)
│
├── .github/
│   ├── agents/
│   │   └── doc-reviewer.agent.md   # Copilot agent definition
│   └── skills/
│       └── confluence-doc-review/
│           └── SKILL.md            # Review guidelines and scoring rubric
│
├── .vscode/
│   └── mcp.json                    # Registers the MCP server with VS Code Copilot
│
├── requirements.txt
└── README.md
```

---

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| VS Code | 1.99+ |
| GitHub Copilot extension | Latest |
| Python | 3.10+ |
| pip / uv | Any recent version |

---

## Setup — Step by Step

### 1. Clone or copy this project
```bash
git clone <your-repo-url>
cd confluence-doc-reviewer
```

### 2. Create a Python virtual environment
You do NOT need a full Python project (no pyproject.toml required).
A simple venv is enough:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Open the project in VS Code
```bash
code .
```

### 5. Register the MCP server with VS Code

VS Code reads `.vscode/mcp.json` automatically.

To verify or start it manually:
1. Open the Command Palette → `Cmd/Ctrl + Shift + P`
2. Type `MCP: List Servers` and press Enter
3. You should see `confluence-doc-review` listed
4. Click **Start** next to it (or it may start automatically)
5. VS Code will prompt you for three values:
   - **Confluence URL** — `https://yourcompany.atlassian.net`
   - **Email** — your Atlassian account email
   - **API Token** — generate one at https://id.atlassian.com/manage-profile/security/api-tokens

> Credentials are stored securely by VS Code's secret storage — never in plain text.

### 6. Verify the MCP server is running

In VS Code, open Copilot Chat (`Ctrl+Alt+I` / `Cmd+Ctrl+I`):
1. Switch to **Agent mode** using the dropdown next to the chat input
2. Click the **🔧 Tools** icon
3. You should see `confluence-doc-review` with three tools:
   - `get_page`
   - `search_pages`
   - `list_pages_in_space`

---

## Using the Agent

In Copilot Chat (Agent mode), invoke the `@doc-reviewer` agent:

```
@doc-reviewer review Confluence page 123456789

@doc-reviewer audit all docs in the ENG space

@doc-reviewer score the documentation for "authentication flow" in PLAT space

@doc-reviewer compare all pages in the API space
```

Copilot will:
1. Call the MCP tool to fetch the page(s)
2. Apply the scoring rubric from the skill
3. Return a structured review with scores, strengths, and recommendations

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| MCP server not listed | Check `.vscode/mcp.json` — root key must be `"servers"` not `"mcpServers"` |
| Server starts but tools not visible | Switch Copilot Chat to **Agent mode** — MCP tools are invisible in Ask/Edit mode |
| Authentication error from Confluence | Regenerate API token at id.atlassian.com; re-enter via `MCP: List Servers` |
| `ModuleNotFoundError: fastmcp` | Run `pip install -r requirements.txt` inside your activated venv |
| VS Code doesn't prompt for credentials | Delete stored secrets via `MCP: List Servers` → server → Reset Inputs |

---

## How It Works

```
You (@doc-reviewer review page 123456789)
        │
        ▼
doc-reviewer.agent.md         ← orchestrates the workflow
        │
        ▼
confluence-doc-review SKILL   ← applies scoring rubric
        │
        ▼
confluence-doc-review MCP     ← calls Confluence REST API
(confluence_server.py)          via FastMCP on stdio
        │
        ▼
Confluence Cloud               ← returns page content
```
