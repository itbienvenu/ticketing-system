/* eslint-disable */
// import { createApp } from "vue";
import Vue from "vue";
/* eslint-disable */

Vue.config.productionTip = false

import App from "./App.vue";
import router from "./router";

new Vue({
    render: h => h(App),
}).$mount("#app")

// createApp(App).use(router).mount("#app");
