import { createApp } from "vue";

import PrimeVue from "primevue/config";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Menubar from "primevue/menubar";
import DataView from "primevue/dataview";

import App from "./App.vue";
import router from "./router";

import "primevue/resources/themes/mdc-dark-indigo/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

import 'primeflex/primeflex.css';

createApp(App)
  .use(PrimeVue)
  .component("InputText", InputText)
  .component("Button", Button)
  .component("Menubar", Menubar)
  .component("DataView", DataView)
  .use(router)
  .mount("#app");
