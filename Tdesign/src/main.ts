import { createApp } from 'vue'
import App from './App.vue';
import TDesign from 'tdesign-vue-next';
import 'tdesign-vue-next/es/style/index.css';
import router from './router'

import './assets/main.css'

const app = createApp(App);

app.use(TDesign);
app.use(router)

app.mount('#app')
