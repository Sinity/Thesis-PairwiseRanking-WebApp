import { createApp } from "vue";

import PrimeVue from "primevue/config";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Menubar from "primevue/menubar";
import Dropdown from "primevue/dropdown";
import DataView from "primevue/dataview";
import DataViewLayoutOptions from "primevue/dataviewlayoutoptions";
import Dialog from "primevue/dialog";
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import MultiSelect from 'primevue/multiselect';
import Panel from 'primevue/panel';
import ToastService from 'primevue/toastservice';
import Toast from 'primevue/toast';

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
  .component("DataViewLayoutOptions", DataViewLayoutOptions)
  .component("Dropdown", Dropdown)
  .component("Dialog", Dialog)
  .component("DataTable", DataTable)
  .component("Column", Column)
  .component("MultiSelect", MultiSelect)
  .component("Panel", Panel)
  .component("Toast", Toast)
  .use(ToastService)
  .use(router)
  .mount("#app");
