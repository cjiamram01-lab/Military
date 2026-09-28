import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  base: '/military-service/',
  plugins: [
    vue(),
    VitePWA({
      devOptions: { enabled: true },
      includeAssets: ['favicon.svg', 'icons.svg'],
      manifest: {
        id: '/military/',
        name: 'ระบบขอผ่อนผันการเกณฑ์ทหาร',
        short_name: 'ผ่อนผันทหาร',
        description: 'ระบบขอผ่อนผันการเกณฑ์ทหารสำหรับนักศึกษา',
        lang: 'th',
        start_url: '/military-service/',
        scope: '/military-service/',
        display: 'standalone',
        background_color: '#f5f7fb',
        theme_color: '#1d4ed8',
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' },
          {
            src: 'icons/icon-maskable-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,ico}'],
      },
    }),
  ],
})
