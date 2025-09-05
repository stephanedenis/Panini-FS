// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Research section', () => {
  test('index and overview exist', async ({ page }) => {
    await page.goto('/research/');
    await expect(page).toHaveTitle(/Recherche|Research/i);
    // Overview page link
    await page.goto('/research/overview/');
    await expect(page.locator('h1')).toContainText(/Recherche|Research/i);
  });

  test('whats-new and feed.xml are live', async ({ page }) => {
    const resp1 = await page.request.get('/research/whats-new.html');
    expect(resp1.status()).toBe(200);
    const resp2 = await page.request.get('/research/feed.xml');
    expect(resp2.status()).toBe(200);
  });
});
