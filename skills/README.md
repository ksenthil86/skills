# BDD + Playwright Test Generator — GitHub Copilot Agent Setup

AI-powered BDD workflow using **1 Orchestrator Agent** + **2 Skills** inside GitHub Copilot.

---

## Project Structure

```
.github/
  copilot-instructions.md              ← Global Playwright + BDD conventions (always active)
  agents/
    bdd-orchestrator.agent.md          ← Master workflow agent
  skills/
    bdd-feature-generator/
      SKILL.md                         ← Gherkin writing expertise
      feature-template.feature         ← Reference example
    glue-code-generator/
      SKILL.md                         ← Playwright step definition expertise
      step-template.ts                 ← Reference example

features/                              ← Generated .feature files go here
steps/                                 ← Generated step definitions go here
pages/                                 ← Generated page object stubs go here
```

---

## Prerequisites

### 1. Enable Agent Skills in VS Code
Open VS Code Settings (`Cmd+,` / `Ctrl+,`) and enable:
```
chat.useAgentSkills: true
```
Or add to your `settings.json`:
```json
{
  "chat.useAgentSkills": true
}
```

### 2. Install Dependencies
```bash
npm install @playwright/test @cucumber/cucumber
npx playwright install
```

### 3. Select the Agent in Copilot Chat
- Open Copilot Chat (`Ctrl+Alt+I`)
- Click the **agent dropdown** at the bottom of the chat panel
- Select **`bdd-orchestrator`**

---

## Usage

### Basic — One Command Does Everything
Switch to the `bdd-orchestrator` agent, then type your story:

```
As a registered user
I want to log into the application
So that I can access my personalised dashboard

Acceptance Criteria:
1. Valid credentials redirect the user to the dashboard
2. Invalid credentials show an error message
3. Empty username shows "Username is required"
4. Empty password shows "Password is required"
5. Locked accounts show "Sorry, this user has been locked out"
6. Username is preserved after a failed login attempt
```

The agent will generate:
- `features/user-login.feature`
- `steps/user-login.steps.ts`
- `pages/user-login.page.ts`

### Trigger the Skills Directly (without the orchestrator)

You can also invoke each skill manually in Copilot Chat:

```
/bdd-feature-generator  generate a feature for password reset
```
```
/glue-code-generator  generate steps for features/password-reset.feature
```

---

## What Gets Generated

### Feature File (`features/<name>.feature`)
- Full Gherkin with `Feature`, `Background`, `Scenario`, `Scenario Outline`
- Tagged with `@smoke`, `@negative`, `@regression`
- One scenario per acceptance criterion
- Data tables for multi-value ACs

### Step Definitions (`steps/<name>.steps.ts`)
- `Given/When/Then` with Cucumber expressions (`{string}`, `{int}`)
- Full browser lifecycle hooks (`BeforeAll`, `Before`, `After`, `AfterAll`)
- Delegates all UI interactions to the Page Object
- `TODO:` comments for selectors needing your input

### Page Object Stub (`pages/<name>.page.ts`)
- Typed locators using `getByRole`, `getByLabel`, `getByText`
- Stubbed action methods (`navigate`, `enterUsername`, `clickLoginButton`)
- `TODO:` comments where real selectors need to be wired up

---

## After Generation — Your Checklist

1. **Fill in selectors** — find all `TODO:` comments in the generated files
2. **Update base URL** — set `baseURL` in `playwright.config.ts`
3. **Add test data** — replace hardcoded credentials with env variables
4. **Run tests**:
   ```bash
   npx cucumber-js features/<name>.feature
   ```

---

## Skill Auto-Detection

Copilot will automatically load the right skill even without the orchestrator agent.
Just describe what you want in plain language:

| You say | Copilot loads |
|---|---|
| "create BDD scenarios for checkout" | `bdd-feature-generator` |
| "generate step definitions for this feature" | `glue-code-generator` |
| "write acceptance tests for login story" | `bdd-orchestrator` agent |

---

## Tips for Best Results

- **Be specific with ACs** — vague criteria ("it should work") will prompt a clarifying question
- **One story at a time** — stories with >8 ACs will be flagged for splitting
- **Paste the whole story** — the more context you give, the better the Gherkin
- **Copilot CLI** — skills also work via `gh copilot` in the terminal
