import { test, expect } from '@playwright/test';

test.describe('Python Deep Dive Lab E2E Suite', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app root
    await page.goto('/');
    // Wait for the app to hydrate and fetch modules
    await page.waitForSelector('text=PyDeep');
    await page.waitForSelector('h1');
  });

  test('1. Should render the application with navigation, curriculum, and first lesson', async ({ page }) => {
    // 1. Brand title
    await expect(page.locator('text=PyDeep').first()).toBeVisible();

    // 2. Mode buttons
    await expect(page.locator('button:has-text("Обучение")')).toBeVisible();
    await expect(page.locator('button:has-text("Песочница")')).toBeVisible();

    // 3. Execution controls
    await expect(page.locator('button:has-text("Запустить")')).toBeVisible();
    await expect(page.locator('button:has-text("Проверить тесты")')).toBeVisible();

    // 4. Curriculum sidebar modules
    await expect(page.locator('text=Модуль 0: Абсолютный старт').first()).toBeVisible();

    // 5. Theory pane active lesson title
    await expect(page.locator('h1:has-text("0.1. Переменные, вычисления и вывод")')).toBeVisible();
  });

  test('2. Should toggle between Curriculum and Sandbox modes', async ({ page }) => {
    // Check initial curriculum theory pane
    await expect(page.locator('h1:has-text("0.1. Переменные, вычисления и вывод")')).toBeVisible();

    // Switch to Sandbox mode
    await page.click('button:has-text("Песочница")');

    // Theory pane should no longer be visible in sandbox mode
    await expect(page.locator('h1:has-text("0.1. Переменные, вычисления и вывод")')).not.toBeVisible();

    // Switch back to Curriculum mode
    await page.click('button:has-text("Обучение")');
    await expect(page.locator('h1:has-text("0.1. Переменные, вычисления и вывод")')).toBeVisible();
  });

  test('3. Should switch lessons within curriculum', async ({ page }) => {
    // Click on lesson 0.2 in curriculum sidebar
    const lesson0_2 = page.locator('button:has-text("0.2. Ветвления и логика")');
    await expect(lesson0_2).toBeVisible();
    await lesson0_2.click();

    // Theory pane title should update
    await expect(page.locator('h1:has-text("0.2. Ветвления и логика")')).toBeVisible();
  });

  test('4. Should progressively unlock hints', async ({ page }) => {
    // Initially no hints are unlocked
    await expect(page.locator('text=Уровень 1:')).not.toBeVisible();

    // Click to unlock Hint 1
    const hintBtn = page.locator('button:has-text("Открыть подсказку 1 из 3")');
    await expect(hintBtn).toBeVisible();
    await hintBtn.click();

    // Hint 1 should now be visible
    await expect(page.locator('text=Уровень 1:')).toBeVisible();

    // Click to unlock Hint 2
    const hint2Btn = page.locator('button:has-text("Открыть подсказку 2 из 3")');
    await expect(hint2Btn).toBeVisible();
    await hint2Btn.click();

    // Hint 2 should now be visible
    await expect(page.locator('text=Уровень 2:')).toBeVisible();
  });

  test('5. Should reveal solution with safety confirmation', async ({ page }) => {
    // Click button to request solution
    const solBtn = page.locator('button:has-text("Не получается решить? Открыть решение")');
    await expect(solBtn).toBeVisible();
    await solBtn.click();

    // Confirmation message appears
    await expect(page.locator('text=Вы уверены? Попробуйте сначала воспользоваться подсказками')).toBeVisible();

    // Click confirm button
    await page.click('button:has-text("Да, показать решение")');

    // Solution code block should appear
    await expect(page.locator('text=Решение открыто')).toBeVisible();
    await expect(page.locator('button:has-text("Вставить в редактор")')).toBeVisible();
  });

  test('6. Should execute code and display stdout in console panel', async ({ page }) => {
    // Click "Запустить" button
    const runBtn = page.locator('button:has-text("Запустить")');
    await expect(runBtn).toBeVisible();
    await runBtn.click();

    // Output tab should show runtime info
    await expect(page.locator('text=Время:')).toBeVisible();
    await expect(page.locator('text=Код возврата:')).toBeVisible();
  });

  test('7. Should run automated tests and display grader results', async ({ page }) => {
    // Click "Проверить тесты" button
    const testBtn = page.locator('button:has-text("Проверить тесты")');
    await expect(testBtn).toBeVisible();
    await testBtn.click();

    // Grader results banner appears in tests tab
    await expect(page.locator('text=Результаты тестов')).toBeVisible();
    await expect(page.locator('text=из 3 тестов')).toBeVisible();
  });

  test('8. Should open File Explorer and Pip Package Manager tabs', async ({ page }) => {
    // Click File Explorer tab icon
    const fileTabBtn = page.locator('button[title="Файловый менеджер проекта"]');
    await expect(fileTabBtn).toBeVisible();
    await fileTabBtn.click();

    await expect(page.locator('text=Файлы проекта')).toBeVisible();
    await expect(page.locator('text=main.py').first()).toBeVisible();

    // Click Pip Packages tab icon
    const pipTabBtn = page.locator('button[title="Менеджер библиотек Pip"]');
    await expect(pipTabBtn).toBeVisible();
    await pipTabBtn.click();

    await expect(page.locator('text=Менеджер пакетов Pip')).toBeVisible();
    await expect(page.locator('text=Популярные для изучения')).toBeVisible();
    await expect(page.locator('text=numpy').first()).toBeVisible();
  });

  test('9. Should open Profile Modal and display progress, accuracy, and achievements tabs', async ({ page }) => {
    // Click Profile button in navbar
    const profileBtn = page.locator('button[title="Профиль пользователя и достижения"]');
    await expect(profileBtn).toBeVisible();
    await profileBtn.click();

    // Profile modal should appear
    await expect(page.locator('text=Pythonista')).toBeVisible();
    await expect(page.locator('text=Точность тестов')).toBeVisible();
    await expect(page.locator('text=Точность решений & Тесты')).toBeVisible();

    // Switch to Achievements tab
    const achTabBtn = page.locator('button:has-text("Ачивки")');
    await expect(achTabBtn).toBeVisible();
    await achTabBtn.click();

    // Verify achievement titles exist
    await expect(page.locator('text=Первый импульс')).toBeVisible();
    await expect(page.locator('text=Снайпер 100%')).toBeVisible();
    await expect(page.locator('text=Магия графиков')).toBeVisible();

    // Close modal
    await page.keyboard.press('Escape');
  });

  test('10. Should accurately update solution test stats and achievements after test execution', async ({ page }) => {
    // Run automated tests for current lesson
    const testBtn = page.locator('button:has-text("Проверить тесты")');
    await expect(testBtn).toBeVisible();
    await testBtn.click();
    await expect(page.locator('text=из 3 тестов')).toBeVisible();

    // Open Profile modal
    const profileBtn = page.locator('button[title="Профиль пользователя и достижения"]');
    await profileBtn.click();

    // Verify lesson stats record appears in accuracy tab
    await expect(page.locator('text=Попыток: 1')).toBeVisible();
    await expect(page.locator('text=Частичный успех')).toBeVisible();
  });
});

