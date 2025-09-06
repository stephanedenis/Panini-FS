// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Modules documentation (aggregated)', () => {
  test('modules index is reachable and titled', async ({ page }) => {
    await page.goto('/modules/');
    await expect(page).toHaveTitle(/Documentation des modules|Module documentation/i);
    await expect(page.locator('h1')).toContainText(/Documentation des modules|Module documentation/i);
  });

  test('aggregated module pages resolve when present, otherwise fallback links exist', async ({ page }) => {
    await page.goto('/modules/');

    // Find potential aggregated links (contain '/modules/_ext/')
    const links = await page.locator('a[href*="/modules/_ext/"]').evaluateAll(as => as.map(a => a.getAttribute('href')));
    const uniqueLinks = Array.from(new Set(links.filter(Boolean)));

    if (uniqueLinks.length > 0) {
      // Probe up to 3 aggregated links, ensuring 200
      const toCheck = uniqueLinks.slice(0, 3).map(href => href.replace(/index\.md$/i, ''));
      for (const href of toCheck) {
        let url = href;
        // Normalize relative links to absolute path for request API
        if (href.startsWith('http')) {
          // Should not be http for aggregated, but keep safe
          url = href;
        } else {
          // Ensure leading slash
          url = href.startsWith('/') ? href : new URL(href, page.url()).pathname;
        }
        // Try canonical folder URL and explicit index.html
        const resp1 = await page.request.get(url);
        const status1 = resp1.status();
        const resp2 = status1 === 404 ? await page.request.get(url.replace(/\/?$/, '/index.html')) : null;
        const ok = status1 === 200 || (resp2 && resp2.status() === 200);
        expect(ok, `Expected 200 for aggregated module page: ${url}`).toBeTruthy();
      }
    } else {
      // Fallback mode: ensure at least one GitHub link is present
      const ghLinks = await page.locator('a[href*="https://github.com/stephanedenis/PaniniFS/"]').count();
      expect(ghLinks).toBeGreaterThan(0);
    }
  });
});
