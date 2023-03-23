import { defineConfig,loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
import vuetify from 'vite-plugin-vuetify'

// https://vitejs.dev/config/
export default defineConfig({

  plugins: [
		vue(),
		vuetify({ autoImport: true }),
	],
	build: {
		outDir: '../dist'
	},
	server: {
		host: true,
		port: 2018
	},
  test: {
    setupFiles: "vuetify.config.js",
    deps: {
      inline: ["vuetify"],
    },
    globals: true,
		environment: "jsdom",
  },
})
