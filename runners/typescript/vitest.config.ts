import { defineConfig } from 'vitest/config'

export default defineConfig({
  cacheDir: '/tmp/.vite',
  test: {
    cache: {
      dir: '/tmp/.vitest'
    }
  }
})
