import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    outDir: "../static",
    rollupOptions: {
      input: {
        indexPage: "./main.js",
      },
      output: {
        assetFileNames: (assetInfo) => {
          if (assetInfo.name.includes(".css")) {
            return "[name].css";
          }

          return assetInfo.name;
        },
        entryFileNames: (fileInfo) => {
          return "[name].js";
        },
      },
    }
  }
})