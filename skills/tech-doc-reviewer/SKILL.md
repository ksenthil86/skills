---
name: confluence-doc-review
description: >
  Reviews Confluence technical documentation pages and scores them against
  review guidelines. Use this skill when asked to review, audit, score, or
  assess the quality of Confluence documentation. Uses a bundled Python
  script to connect to Confluence directly — no MCP server required.
---

# Confluence Documentation Review Skill

## Overview
This skill fetches Confluence pages by running the bundled `confluence_fetch.py`
script directly. No external servers or MCP setup required. Authentication is
handled via environment variables.

---

## Prerequisites

### 1. Install the dependency
```bash
pip install requests
```

### 2. Set environment variables
```bash
export CONFLUENCE_URL="https://yourcompany.atlassian.net"
export CONFLUENCE_EMAIL="you@company.com"
export CONFLUENCE_API_TOKEN="your-atlassian-api-token"
```

> **How to get an API token:** Log in to Atlassian → Account Settings →
> Security → Create and manage API tokens.

---

## Step 1 — Fetch the Confluence Page

Run the bundled script from this skill's directory using one of these commands:

### Fetch a page by ID
```bash
python .github/skills/confluence-doc-review/confluence_fetch.py page <PAGE_ID>
```

### Search pages by keyword
```bash
python .github/skills/confluence-doc-review/confluence_fetch.py search "<KEYWORD>" [SPACE_KEY]
```

### List all pages in a space
```bash
python .github/skills/confluence-doc-review/confluence_fetch.py list <SPACE_KEY>
```

> The script prints JSON to stdout. Parse the `title`, `body`, `url`,
> `version`, `author`, and `last_modified` fields for the review.

---

## Step 2 — Review Against Guidelines

Analyse the page content using the following **10 criteria**, each scored
out of 10:

| # | Criterion | What to check |
|---|-----------|---------------|
| 1 | **Purpose & Scope** | Clear intro explaining what the doc covers and who it is for |
| 2 | **Completeness** | All major aspects covered; no obvious gaps |
| 3 | **Accuracy** | Technically correct and up to date |
| 4 | **Clarity** | Plain language, minimal unnecessary jargon |
| 5 | **Structure** | Logical headings, sections, and hierarchy |
| 6 | **Code Examples** | Snippets included where appropriate and correct |
| 7 | **Visuals & Diagrams** | Diagrams or screenshots used where they add value |
| 8 | **Links & References** | Cross-references and external links present and valid |
| 9 | **Maintainability** | Owner listed, version noted, last-reviewed date present |
| 10 | **Actionability** | Reader can act on this without needing extra help |

---

## Step 3 — Output the Review

Produce the review in this exact format:

---

### 📄 Documentation Review: [Page Title]
**URL:** [Confluence page URL]  
**Space:** [Space key]  
**Version:** [version number]  
**Author:** [last modified by]  
**Last Modified:** [date]  
**Reviewed on:** [today's date]

#### Scores

| Criterion | Score | Notes |
|-----------|-------|-------|
| Purpose & Scope | x/10 | … |
| Completeness | x/10 | … |
| Accuracy | x/10 | … |
| Clarity | x/10 | … |
| Structure | x/10 | … |
| Code Examples | x/10 | … |
| Visuals & Diagrams | x/10 | … |
| Links & References | x/10 | … |
| Maintainability | x/10 | … |
| Actionability | x/10 | … |

#### **Overall Score: XX / 100**

#### Grade
| Score Range | Grade |
|-------------|-------|
| 90–100 | ⭐ Excellent |
| 75–89  | ✅ Good |
| 60–74  | ⚠️ Needs Improvement |
| Below 60 | 🔴 Poor — immediate action required |

#### ✅ Strengths
- [Specific things the doc does well]

#### ⚠️ Recommendations
- [Specific, actionable suggestions — reference section names where possible]

#### 🔴 Critical Issues
- [Anything blocking the doc from being usable — or "None" if all clear]

---

## Step 4 — Multiple Page Review (optional)

If reviewing multiple pages (e.g. from a `list` command), produce individual
reviews for each page and then append a **Comparative Summary** table:

| Page | Score | Grade | Top Issue |
|------|-------|-------|-----------|
| Page A | 82/100 | ✅ Good | Missing code examples |
| Page B | 54/100 | 🔴 Poor | No structure, outdated |
| Page C | 91/100 | ⭐ Excellent | Minor link issues |
