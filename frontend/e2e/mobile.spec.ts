import { test, expect } from '@playwright/test';

test.describe('Mobile Viewport UX Suite (390x844)', () => {
  test.use({
    viewport: { width: 390, height: 844 },
    hasTouch: true,
    isMobile: true,
  });

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForSelector('button[title="Открыть меню"]');
    await page.waitForSelector('h1');
  });

  test('1. Should display mobile navigation bar with hamburger menu and view switcher', async ({ page }) => {
    // Brand should show PyDeep
    await expect(page.locator('text=PyDeep').first()).toBeVisible();

    // Hamburger menu button should be visible on mobile
    const menuBtn = page.locator('button[title="Открыть меню"]');
    await expect(menuBtn).toBeVisible();

    // Mobile tabs switcher should be visible at top
    await expect(page.locator('button:has-text("Теория & Задание")')).toBeVisible();
    await expect(page.locator('button:has-text("Редактор кода")')).toBeVisible();
    await expect(page.locator('button:has-text("Консоль / Тесты")')).toBeVisible();

    // Theory pane should be visible and readable
    await expect(page.locator('h1:has-text("1.1. Ссылочная модель")')).toBeVisible();
  });

  test('2. Should open and close off-canvas drawer on mobile', async ({ page }) => {
    // Tap hamburger menu
    await page.click('button[title="Открыть меню"]');

    // Drawer should appear with navigation tabs
    await expect(page.locator('button:has-text("Курс")')).toBeVisible();
    await expect(page.locator('button:has-text("Файлы")')).toBeVisible();
    await expect(page.locator('button:has-text("Pip")')).toBeVisible();

    // Click on lesson 1.2 inside the drawer
    await page.click('button:has-text("1.2. Области видимости LEGB")');

    // Drawer should automatically close and theory pane should show lesson 1.2
    await expect(page.locator('h1:has-text("1.2. Области видимости LEGB")')).toBeVisible();
  });

  test('3. Should seamlessly switch views using mobile tabs and jump to editor button', async ({ page }) => {
    // Click "Перейти к решению в редакторе" button at bottom of theory pane
    const ctaBtn = page.locator('button:has-text("Перейти к решению в редакторе →")');
    await expect(ctaBtn).toBeVisible();
    await ctaBtn.click();

    // Editor should now be active
    await expect(page.locator('.monaco-editor')).toBeVisible();

    // Switch to Console tab
    await page.click('button:has-text("Консоль / Тесты")');
    await expect(page.locator('text=Консоль вывода')).toBeVisible();

    // Switch back to Theory tab
    await page.click('button:has-text("Теория & Задание")');
    await expect(page.locator('h1:has-text("1.1. Ссылочная модель")')).toBeVisible();
  });

  test('4. Should run code on mobile and auto-navigate to console view', async ({ page }) => {
    // Tap "Запустить" in header
    await page.click('button:has-text("Запустить")');

    // Should automatically switch to console view and display execution results
    await expect(page.locator('text=Время:')).toBeVisible();
    await expect(page.locator('text=Код возврата:')).toBeVisible();
  });
});
