import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/templates",
      name: "templates",
      component: () => import("../views/TemplateView.vue"),
    },
    {
      path: "/templates/create",
      name: "templates.create",
      component: () => import("../views/CreateTemplateView.vue"),
    },
    {
      path: "/subscriptions",
      name: "subscriptions",
      component: () => import("../views/SubscriptionsView.vue"),
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
  ],
});

export default router;
