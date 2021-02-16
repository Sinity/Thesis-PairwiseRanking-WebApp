import { createApp } from "vue";

import PrimeVue from "primevue/config";
import InputText from "primevue/inputtext";
import Button from "primevue/button";

import App from "./App.vue";
import router from "./router";

import "primevue/resources/themes/saga-blue/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

createApp(App)
  .use(PrimeVue)
  .component("InputText", InputText)
  .component("Button", Button)
  .use(router)
  .mount("#app");
