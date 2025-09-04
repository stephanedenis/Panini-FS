// @ts-check
const { test, expect } = require('@playwright/test');

test('homepage loads and shows title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Pāṇini File System/i);
  await expect(page.locator('h1')).toContainText('Pāṇini File System');
});

test('navigation has Recherche and Modules docs', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('link', { name: /Recherche/i })).toBeVisible();
  await expect(page.getByRole('link', { name: /Modules/ })).toBeVisible();
});
