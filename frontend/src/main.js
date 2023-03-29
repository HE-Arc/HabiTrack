import { createApp } from "vue";
import { Quasar } from "quasar";
import axios from "axios";
import Cookies from "js-cookie";

// Import icon libraries
import "@quasar/extras/material-icons/material-icons.css";

// Import Quasar css
import "quasar/src/css/index.sass";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

app.use(router);
app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
});

// Set config defaults when creating the instance

axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;

// Add a request interceptor
axios.interceptors.request.use(
  function (config) {
    config.headers["X-CSRFToken"] = Cookies.get("csrftoken");
    config.withCredentials = true;
    return config;
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error);
  }
);

app.mount("#app");
