import { createApp } from "vue";
import { Quasar, Notify } from "quasar";
import axios from "axios";

// Import icon libraries
import "@quasar/extras/material-icons/material-icons.css";

// Import Quasar css
import "quasar/src/css/index.sass";

import App from "./App.vue";
import router from "./router";
import Cookies from "js-cookie";
import "./assets/main.css";

const app = createApp(App);

app.use(router);
app.use(Quasar, {
  plugins: { Notify }, // import Quasar plugins and add here
});

// Set config defaults when creating the instance
axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const csrftoken = Cookies.get("csrftoken");
if (csrftoken == undefined) {
  axios.get("csrf/").then((response) => {
    Cookies.set("csrftoken", response.data.csrfToken, {
      expires: 1 / 48,
    });
  });
}

console.log(csrftoken);
if (csrftoken) {
  axios.defaults.headers.common["X-CSRFToken"] = csrftoken;
} else {
  throw new Error("CSRF token not found - maybe you need to enable cookies?");
}


axios.defaults.withCredentials = true;

app.mount("#app");
