import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
   server: {
     host: '0.0.0.0',
     port: 3000,
      proxy: {
        '/api': {
          target: process.env.BACKEND_URL || 'http://localhost:5000',
          changeOrigin: true
        }
      }
   },
   build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'esbuild',
    target: 'es2015',
    cssCodeSplit: true,
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  }
})