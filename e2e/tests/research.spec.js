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

  test('whats-new and feed.xml should be live soon (currently 404)', async ({ page }) => {
    const resp1 = await page.request.get('/research/whats-new.html');
    expect([200, 404]).toContain(resp1.status());
    const resp2 = await page.request.get('/research/feed.xml');
    expect([200, 404]).toContain(resp2.status());
    // TODO: switch to expect 200 once Pages workflow includes RSS generation output
  });
});
