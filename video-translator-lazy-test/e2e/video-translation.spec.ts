import { test, expect } from '@playwright/test';
import path from 'path';

test.use({ video: 'on' });

// Test data structure
const testCases = [
  {
    fixture: 'ytTest1.mp4',
    targetLang: 'German',
    targetLangCode: 'de',
    expectWarning: false, 
    emptyAudio: false
  },
  {
    fixture: 'empty_audio.mp4', 
    targetLang: 'Malay',
    targetLangCode: 'ms',
    expectWarning: true,
    emptyAudio: true
  },
  {
    fixture: 'mixed_lang.mp4',
    targetLang: 'English',
    targetLangCode: 'en',
    expectWarning: true,
    emptyAudio: false
  },
];

test.describe('Video Translation - All Languages', () => {
  for (const { fixture, targetLang, expectWarning, emptyAudio } of testCases) {
    test(`${fixture} → ${targetLang}`, async ({ page }) => {
      await page.goto('/');
      
      // 1. Upload
      const fileInput = page.locator('input[type="file"]');
      await fileInput.setInputFiles(path.join(__dirname, 'fixtures', fixture));
      
      // 2. Select target language (don't care about source)
      await page.locator('[data-slot="select-trigger"]').last().click();
      await page.locator(`text=${targetLang}`).click();
      // await page.locator(`[data-slot="select-item"]:has-text(${targetLang})`).click();
      
      // 3. Translate
      await page.click('button:has-text("Translate Video")');

      // Wait for the actual result UI (video OR error card)
      await page.locator('video, [class*="border-red"]').first().waitFor({ 
        timeout: 300000,
        state: 'visible'
      });
      
      // Now verify - video XOR error
      const hasVideo = await page.locator('video').isVisible();
      const hasError = await page.locator('[class*="border-red"]').isVisible();

      if (emptyAudio) {
        // Expect error for empty audio
        if (hasError) {
          console.log('[OK] Empty audio correctly rejected');
          await expect(page.locator('[class*="border-red"]')).toBeVisible();
        } else {
          throw new Error('Expected error for empty audio, but got video');
        }
      } else {
        // Expect video
        if (hasVideo) {
          console.log('[OK] Video generated successfully');
          await expect(page.locator('video')).toBeVisible();
          await expect(page.locator('text=Download Video')).toBeVisible();
        } else if (hasError) {
          const errorText = await page.locator('[class*="text-red"]').textContent();
          throw new Error(`Expected video but got error: ${errorText}`);
        }
      }
      
      // 6. Optional: Check warning if expected
      if (expectWarning && !emptyAudio) {
        await expect(page.locator('text=Mixed Language')).toBeVisible();
      }
      
    });
  }
});