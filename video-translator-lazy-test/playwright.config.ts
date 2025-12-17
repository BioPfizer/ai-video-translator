import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './e2e',
  timeout: 180000,  // 3 minutes per test
  
  use: {
    // Switch between local and production
    baseURL: process.env.TEST_URL || 'http://localhost:3000',
    
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
    
    actionTimeout: 10000,
  },

  // Auto-start dev server for local testing
  webServer: process.env.TEST_URL ? undefined : [
  {
    command: 'cd ../video-translator-frontend && npm run dev',
    url: 'http://localhost:3000',
    timeout: 120000,
    reuseExistingServer: true,
  },
  {
    command: 'cd ../video-translator-api && start-elvet.bat',
    url: 'http://localhost:8000',
    timeout: 120000,
    reuseExistingServer: true,
  }
],

//   // Auto-start dev server for local testing
//   webServer: process.env.TEST_URL ? undefined : [
//   {
//     command: 'cd ../video-translator-frontend && npm run dev',
//     url: 'http://localhost:3000',
//     timeout: 120000,
//     reuseExistingServer: true,
//   }

// ],
  
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  
  reporter: [
    ['html'],
    ['list'],
  ],
});