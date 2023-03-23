import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';
import "./style.css"

loadFonts()

const app = createApp(App);
app.component('EasyDataTable', Vue3EasyDataTable);

app.use(router)
  .use(vuetify)
  .mount('#app')
