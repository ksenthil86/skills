# Copilot Workspace Instructions

## Project Context
This is a Playwright end-to-end test project using BDD (Behaviour-Driven Development).
All test scenarios are written in Gherkin and implemented as Playwright TypeScript step definitions.

## BDD Conventions
- Feature files live in `features/` directory
- Step definitions live in `steps/` directory
- File naming: `<feature-name>.feature` and `<feature-name>.steps.ts`
- One feature file per user story
- Steps must be reusable across scenarios where possible
- Use Background for shared preconditions within a feature

## Playwright Conventions
- Use TypeScript strictly — no `any` types
- Use the Page Object Model (POM) — page classes live in `pages/`
- Prefer `page.getByRole()`, `page.getByLabel()`, `page.getByText()` over CSS selectors
- Always use `await expect(locator).toBeVisible()` before interacting
- Use `test.step()` inside Playwright for nested reporting
- Timeouts: default 30s, network calls 10s
- Never use `page.waitForTimeout()` — use `expect` with polling instead

## TypeScript Conventions
- Use `async/await` throughout
- Imports: group Node, third-party, local — separated by blank lines
- All step definition files must import from `@cucumber/cucumber`
- Fixtures are defined in `fixtures/` and extended from `@playwright/test`

## Output Directories
- `features/`    → Gherkin feature files
- `steps/`       → Cucumber step definitions
- `pages/`       → Playwright page objects
- `fixtures/`    → Playwright test fixtures
