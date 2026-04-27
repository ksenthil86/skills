---
name: confluence-doc-review
description: >
  Reviews Confluence technical documentation pages and scores them against
  review guidelines. Activates when asked to review, audit, score, or assess
  Confluence docs. Connects via the local confluence-doc-review MCP server.
---

# Confluence Documentation Review Skill

## What This Skill Does
Fetches Confluence pages through the local MCP server and scores them across
10 quality criteria, producing a structured review with an overall score out
of 100 and actionable recommendations.

---

## Step 1 — Identify What to Review

Determine which tool to call based on what the user provided:

| User provides | Tool to call |
|---|---|
| A page ID (e.g. `123456789`) | `get_page` |
| A Confluence URL | Extract the page ID from the URL, then call `get_page` |
| A keyword or topic | `search_pages`, then confirm with user which page to review |
| A space key (e.g. `ENG`) | `list_pages_in_space`, then review each page or ask user to pick |

---

## Step 2 — Score Against Review Guidelines

Analyse the page body against these **10 criteria**, each scored out of 10:

| # | Criterion | What to look for |
|---|-----------|------------------|
| 1 | **Purpose & Scope** | Clear intro stating what the doc covers and who it is for |
| 2 | **Completeness** | All key aspects covered; no obvious gaps |
| 3 | **Accuracy** | Technically correct; content appears up to date |
| 4 | **Clarity** | Plain language; minimal unnecessary jargon |
| 5 | **Structure** | Logical headings and hierarchy; easy to navigate |
| 6 | **Code Examples** | Snippets provided where relevant; examples are correct |
| 7 | **Visuals & Diagrams** | Diagrams or screenshots used where they add value |
| 8 | **Links & References** | Cross-references and external links present and accurate |
| 9 | **Maintainability** | Owner listed; version noted; last-reviewed date present |
| 10 | **Actionability** | Reader can act without needing extra help |

---

## Step 3 — Produce the Review

Output the review in this exact format:

---

### 📄 Documentation Review: [Page Title]
**URL:** [page URL]
**Space:** [space key — space name]
**Version:** [version number] · **Author:** [last author] · **Last Modified:** [date]
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

#### Overall Score: **XX / 100**

| Score | Grade |
|-------|-------|
| 90–100 | ⭐ Excellent |
| 75–89 | ✅ Good |
| 60–74 | ⚠️ Needs Improvement |
| < 60 | 🔴 Poor — immediate action required |

#### ✅ Strengths
- [What the doc does well — be specific]

#### ⚠️ Recommendations
- [Actionable suggestions referencing specific sections]

#### 🔴 Critical Issues
- [Blockers to usability — or write "None"]

---

## Step 4 — Multi-Page Comparative Summary (optional)

If reviewing multiple pages, append this table after the individual reviews:

| Page | Score | Grade | Top Issue |
|------|-------|-------|-----------|
| [title] | XX/100 | … | … |
