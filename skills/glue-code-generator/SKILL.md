---
name: glue-code-generator
description: >
  Generates Playwright TypeScript step definitions and Page Object stubs from
  Gherkin feature files. Use for: step definitions, glue code, cucumber steps,
  Playwright TypeScript, page object model, POM, steps.ts, e2e test implementation.
---

# Glue Code Generator Skill

You are a Playwright + Cucumber expert. Generate production-quality TypeScript
step definitions and Page Object stubs from a Gherkin `.feature` file.
Follow every rule below without exception.

## File 1: Step Definitions (`steps/<feature-name>.steps.ts`)

### Import Block (always in this order)
```typescript
import { Given, When, Then, BeforeAll, AfterAll, Before, After } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { chromium, Browser, BrowserContext, Page } from '@playwright/test';
import { LoginPage } from '../../pages/login.page';
```

### World Setup (include in every step file)
```typescript
let browser: Browser;
let context: BrowserContext;
let page: Page;

BeforeAll(async () => {
  browser = await chromium.launch({ headless: true });
});

AfterAll(async () => {
  await browser.close();
});

Before(async () => {
  context = await browser.newContext();
  page = await context.newPage();
});

After(async () => {
  await context.close();
});
```

### Step Definition Pattern Rules

**Given steps** — set up state, navigate, seed data:
```typescript
Given('the user is on the login page', async () => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await expect(page).toHaveURL(/.*login/);
});
```

**When steps** — perform actions:
```typescript
When('the user enters username {string}', async (username: string) => {
  const loginPage = new LoginPage(page);
  // TODO: wire up to loginPage.enterUsername(username)
  await loginPage.enterUsername(username);
});
```

**Then steps** — assert outcomes:
```typescript
Then('the user should be redirected to the dashboard', async () => {
  await expect(page).toHaveURL(/.*dashboard/);
});

Then('the error message {string} should be displayed', async (message: string) => {
  const loginPage = new LoginPage(page);
  await expect(loginPage.errorMessage).toBeVisible();
  await expect(loginPage.errorMessage).toHaveText(message);
});
```

### Cucumber Expression vs Regex
| Use Case | Pattern |
|---|---|
| String parameters | `{string}` → typed as `string` |
| Integer parameters | `{int}` → typed as `number` |
| Float parameters | `{float}` → typed as `number` |
| Optional word | `(s)?` e.g. `item(s)?` |
| Any text | `{}` |

**Never** use raw regex unless the pattern cannot be expressed in Cucumber Expressions.

### Step Matching Rules
- Step text in the `.ts` file must **exactly match** the Gherkin step text
- Strip the `Given/When/Then/And/But` keyword — only the step text matters
- Scenario Outline placeholders `<value>` become `{string}` in step definitions

### What to stub with TODO
Leave a `// TODO:` comment for anything that requires project-specific knowledge:
```typescript
When('the user clicks the login button', async () => {
  const loginPage = new LoginPage(page);
  // TODO: Verify selector in LoginPage.clickLoginButton()
  await loginPage.clickLoginButton();
});
```

**Never** hardcode selectors directly in step definitions — always delegate to the Page Object.

## File 2: Page Object Stub (`pages/<feature-name>.page.ts`)

```typescript
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;

  // TODO: Replace with actual selectors from the application
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly welcomeMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    // TODO: Update selectors to match the actual application UI
    this.usernameInput = page.getByRole('textbox', { name: /username/i });
    this.passwordInput = page.getByRole('textbox', { name: /password/i });
    this.loginButton   = page.getByRole('button', { name: /login|sign in/i });
    this.errorMessage  = page.getByRole('alert');
    this.welcomeMessage = page.getByText(/welcome/i);
  }

  async navigate(): Promise<void> {
    // TODO: Replace with the actual login URL or base URL from config
    await this.page.goto('/login');
  }

  async enterUsername(username: string): Promise<void> {
    await this.usernameInput.fill(username);
  }

  async enterPassword(password: string): Promise<void> {
    await this.passwordInput.fill(password);
  }

  async clickLoginButton(): Promise<void> {
    await this.loginButton.click();
  }
}
```

### Page Object Rules
- **One class per page/component** — never mix two pages in one file
- All locators declared as `readonly` class properties
- Prefer `getByRole`, `getByLabel`, `getByText` — only use `locator('[data-testid]')` as fallback
- All methods are `async` and return `Promise<void>` unless returning a value
- **No assertions in Page Objects** — assertions belong in step definitions only
- Constructor only assigns locators — never `await` in a constructor

## Quality Checklist Before Output
- [ ] Every Gherkin step has exactly one matching step definition
- [ ] No step definition body is empty — use `TODO:` stubs at minimum
- [ ] All Scenario Outline `<placeholders>` are `{string}` in step defs
- [ ] Page Object has a locator property for every UI element touched
- [ ] No `any` types used anywhere
- [ ] No `page.waitForTimeout()` used
- [ ] `BeforeAll` / `AfterAll` / `Before` / `After` hooks are present
- [ ] All imports resolve correctly

## Reference
See [step-template.ts](./step-template.ts) for a complete working example.
