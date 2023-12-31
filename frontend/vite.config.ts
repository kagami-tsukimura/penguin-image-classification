import react from '@vitejs/plugin-react-swc';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    assetsDir: './assets',
  },
  plugins: [react()],
  base: process.env.GITHUB_PAGES ? 'penguin-image-classification/' : './',
});
