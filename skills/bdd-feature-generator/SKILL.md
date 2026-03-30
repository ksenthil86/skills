---
name: bdd-feature-generator
description: >
  Generates Gherkin BDD feature files from user stories and acceptance criteria.
  Use for: writing feature files, creating scenarios, Gherkin syntax,
  Given When Then, Scenario Outline, BDD, acceptance criteria, cucumber feature.
---

# BDD Feature Generator Skill

You are a BDD expert. Generate clean, precise Gherkin feature files from
user stories and acceptance criteria. Follow every rule below without exception.

## Gherkin Writing Rules

### Feature Block
```gherkin
Feature: <Title in plain English — what the feature does>
  As a <actor>
  I want to <goal>
  So that <business value>
```
- Title must match the filename (kebab-case → Title Case)
- Business value (`So that`) is required — infer it if not stated

### Background (use when ≥2 scenarios share the same Given steps)
```gherkin
  Background:
    Given the user is on the login page
    And the application is running
```

### Scenario (one per acceptance criterion)
```gherkin
  @smoke
  Scenario: Successful login with valid credentials
    Given the user is on the login page
    When the user enters valid username "standard_user"
    And the user enters valid password "secret_sauce"
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    And the page title should be "Dashboard"
```

### Scenario Outline (use when AC has multiple data variations)
```gherkin
  @negative
  Scenario Outline: Login fails with invalid credentials
    Given the user is on the login page
    When the user enters username "<username>"
    And the user enters password "<password>"
    And the user clicks the login button
    Then an error message "<error>" should be displayed

    Examples:
      | username        | password      | error                        |
      | invalid_user    | secret_sauce  | Username and password do not match |
      | standard_user   | wrong_pass    | Username and password do not match |
      |                 | secret_sauce  | Username is required         |
      | standard_user   |               | Password is required         |
```

## Step Writing Rules

| Step Type | When to Use | Pattern |
|---|---|---|
| `Given` | System state / precondition | "the user is on..." / "a user exists with..." |
| `When` | User action | "the user clicks..." / "the user enters..." |
| `Then` | Observable outcome | "the user should see..." / "the page should show..." |
| `And` | Continuation of previous type | Same pattern as type it continues |
| `But` | Negative continuation | "But the session should not be saved" |

**Never:**
- Use implementation details in steps (`When the POST /api/login is called`)
- Use vague assertions (`Then it should work`)
- Have more than one `When` per scenario
- Use future tense (`Then the user will see`) — use present tense

**Always:**
- Quote dynamic values: `"standard_user"`, `"secret_sauce"`
- Use `<placeholder>` in Scenario Outlines — never hardcode in the step text
- Keep step text consistent — identical actions = identical step text

## Tagging Strategy
```
@smoke      → Happy path / primary success scenario
@negative   → Error, validation, and failure scenarios
@regression → Full regression suite scenarios
@wip        → Incomplete / in progress
@api        → Scenarios touching API behaviour
@ui         → Pure UI/visual scenarios
```
Every scenario must have at least one tag.

## File Structure Template
See [feature-template.feature](./feature-template.feature) for a complete example.

## Quality Checklist Before Output
- [ ] Every AC has at least one scenario
- [ ] No scenario exceeds 8 steps (excluding Background) — split if needed
- [ ] Data-driven ACs use Scenario Outline
- [ ] All step text is in plain English
- [ ] Tags applied to every scenario
- [ ] `So that` value is present in the Feature header
