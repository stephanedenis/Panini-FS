// @ts-check
/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  timeout: 30000,
  retries: 1,
  use: {
    baseURL: process.env.BASE_URL || 'https://paninifs.org',
    trace: 'on-first-retry',
  },
  reporter: [['list'], ['html', { open: 'never' }]],
};

module.exports = config;
