const { test, expect } = require('@playwright/test');
const path = require('path');

test('Visualiser la page PaniniFS avec texture alvéolaire', async ({ page }) => {
  // Chemin vers notre fichier HTML local
  const htmlPath = path.join(__dirname, '../../assets/index.html');
  const fileUrl = `file://${htmlPath}`;
  
  console.log(`📍 Ouverture de: ${fileUrl}`);
  
  // Aller à la page
  await page.goto(fileUrl);
  
  // Attendre que la page soit chargée
  await page.waitForLoadState('networkidle');
  
  // Vérifier que le titre est présent
  await expect(page.locator('h1')).toContainText('PaniniFS');
  
  // Vérifier que le logo hexagonal est présent
  await expect(page.locator('.logo')).toBeVisible();
  
  // Vérifier que la navigation hexagonale est présente
  await expect(page.locator('.hex-nav')).toBeVisible();
  
  // Vérifier qu'on a bien 6 modules
  const hexItems = page.locator('.hex-item');
  await expect(hexItems).toHaveCount(6);
  
  // Prendre une capture d'écran pour visualiser
  await page.screenshot({ 
    path: 'e2e-results/paniniFS-page.png', 
    fullPage: true 
  });
  
  console.log('✅ Capture d\'écran sauvée dans e2e-results/paniniFS-page.png');
  
  // Tester l'interaction avec un hexagone
  await page.hover('.hex-item:first-child');
  await page.screenshot({ 
    path: 'e2e-results/paniniFS-hover.png',
    fullPage: true 
  });
  
  console.log('✅ Capture avec hover sauvée dans e2e-results/paniniFS-hover.png');
  
  // Vérifier la présence de la texture de fond
  const bodyStyles = await page.evaluate(() => {
    const body = document.body;
    const computedStyles = window.getComputedStyle(body, '::before');
    return {
      backgroundImage: computedStyles.backgroundImage,
      backgroundColor: computedStyles.backgroundColor
    };
  });
  
  console.log('🎨 Styles du fond:', bodyStyles);
  
  // Mesurer les dimensions de la page
  const dimensions = await page.evaluate(() => ({
    width: document.body.scrollWidth,
    height: document.body.scrollHeight
  }));
  
  console.log('📐 Dimensions de la page:', dimensions);
});
