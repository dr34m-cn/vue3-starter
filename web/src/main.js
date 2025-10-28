import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "element-plus/theme-chalk/dark/css-vars.css";
import "@/assets/style/css-vars.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import App from "./App.vue";
import { MotionPlugin } from "@vueuse/motion";
import pinia from "./store";
import router from "./router";
import i18n from "./utils/i18n";
const app = createApp(App);

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(pinia);
app.use(router);
app.use(i18n);
app.use(ElementPlus);
app.use(MotionPlugin);

import { useAppStore } from "@/store/useAppStore";
const appStore = useAppStore();
app.config.globalProperties.$store = appStore;
window.$store = appStore;

app.mount("#app");
