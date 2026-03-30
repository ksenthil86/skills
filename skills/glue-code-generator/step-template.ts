import { Given, When, Then, BeforeAll, AfterAll, Before, After } from '@cucumber/cucumber';
import { expect, chromium, Browser, BrowserContext, Page } from '@playwright/test';
import { LoginPage } from '../../pages/login.page';

// ─── Browser Lifecycle ───────────────────────────────────────────────────────

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

// ─── Given Steps (Preconditions) ─────────────────────────────────────────────

Given('the application is running', async () => {
  // TODO: Add health check or base URL verification if needed
  await expect(page.url()).toBeDefined();
});

Given('the user is on the login page', async () => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await expect(page).toHaveURL(/.*login/);
});

Given('the user is logged in as {string}', async (username: string) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  // TODO: Replace with actual test credentials from environment config
  await loginPage.enterUsername(username);
  await loginPage.enterPassword(process.env.TEST_PASSWORD ?? 'secret_sauce');
  await loginPage.clickLoginButton();
  await expect(page).toHaveURL(/.*dashboard/);
});

// ─── When Steps (Actions) ─────────────────────────────────────────────────────

When('the user enters username {string}', async (username: string) => {
  const loginPage = new LoginPage(page);
  await loginPage.enterUsername(username);
});

When('the user enters password {string}', async (password: string) => {
  const loginPage = new LoginPage(page);
  await loginPage.enterPassword(password);
});

When('the user clicks the login button', async () => {
  const loginPage = new LoginPage(page);
  // TODO: Verify loginButton selector in LoginPage is correct for your app
  await loginPage.clickLoginButton();
});

When('the user clicks the logout button', async () => {
  // TODO: Implement LogoutPage or add logout locator to LoginPage
  const logoutButton = page.getByRole('button', { name: /logout|sign out/i });
  await expect(logoutButton).toBeVisible();
  await logoutButton.click();
});

// ─── Then Steps (Assertions) ──────────────────────────────────────────────────

Then('the user should be redirected to the dashboard', async () => {
  await expect(page).toHaveURL(/.*dashboard/);
});

Then('the welcome message {string} should be displayed', async (message: string) => {
  const loginPage = new LoginPage(page);
  await expect(loginPage.welcomeMessage).toBeVisible();
  await expect(loginPage.welcomeMessage).toHaveText(message);
});

Then('the error message {string} should be displayed', async (errorText: string) => {
  const loginPage = new LoginPage(page);
  await expect(loginPage.errorMessage).toBeVisible();
  await expect(loginPage.errorMessage).toHaveText(errorText);
});

Then('the user should remain on the login page', async () => {
  await expect(page).toHaveURL(/.*login/);
});

Then('the user should be redirected to the login page', async () => {
  await expect(page).toHaveURL(/.*login/);
});

Then('the session should be cleared', async () => {
  // TODO: Verify session cookie or localStorage is cleared
  const cookies = await context.cookies();
  const sessionCookie = cookies.find(c => c.name === 'session');
  expect(sessionCookie).toBeUndefined();
});

Then('the username field should still contain {string}', async (username: string) => {
  const loginPage = new LoginPage(page);
  await expect(loginPage.usernameInput).toHaveValue(username);
});

Then('the password field should be cleared', async () => {
  const loginPage = new LoginPage(page);
  await expect(loginPage.passwordInput).toHaveValue('');
});
